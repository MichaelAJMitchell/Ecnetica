"""
Custom Study System for MCQ Algorithm
Extends the existing MCQScheduler with custom study features including:
- Chapter/node selection
- Prerequisite chain analysis with BFS
- Skills-focused question selection
- Weak area identification using graph theory
- Tomorrow's due question preview
- Intelligent question sequencing with interleaving
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Set, Tuple, Optional, Union, Any
from dataclasses import dataclass, field
from datetime import datetime
import random
from mcq_algorithm_current import (
    MCQScheduler, OptimizedMCQVector, BayesianKnowledgeTracing,
    StudentProfile, KnowledgeGraph, StudentManager
)


@dataclass
class CustomStudyRequest:
    """
    Configuration for custom study sessions.
    Allows students to specify their learning preferences and focus areas.
    """
    # Student selections
    selected_chapters: Optional[List[str]] = None  # ["algebra", "geometry"]
    selected_nodes: Optional[List[int]] = None     # [1, 5, 7, 12] - specific topic IDs
    num_questions: int = 10

    # Focus areas
    skill_focus: Optional[str] = None    # "procedural_fluency", "conceptual_understanding", etc.
    difficulty_preference: str = "balanced"  # "simple", "challenge", "balanced"
    focus_weak_areas: bool = False
    review_due_tomorrow: bool = False

    # Advanced options
    interleaving_preference: float = 0.5  # 0=clustered, 1=fully interleaved- how mixed up topics are
    prerequisite_testing: bool = True

    # Computational limits
    max_prerequisite_depth: int = 4
    max_prerequisite_nodes: int = 100
    max_dfs_nodes: int = 50
    skill_focus_threshold: float = 0.6


class CustomStudyScheduler(MCQScheduler):
    """
    Extended MCQ scheduler for custom study sessions.
    Inherits all functionality from MCQScheduler and adds custom study features.
    """

    def __init__(self, knowledge_graph: KnowledgeGraph, student_manager: StudentManager, bkt_system=None):
        super().__init__(knowledge_graph, student_manager)
        self._centrality_cache = {}  # Cache expensive centrality calculations
        self.bkt_system = bkt_system
        # Precompute expensive graph metrics once
        print("🔄 Precomputing graph metrics for custom study...")
        self._precomputed_metrics = self._precompute_graph_metrics()
        print("✅ Graph metrics precomputed")

    def _precompute_graph_metrics(self) -> Dict:
        """
        Pre-compute all expensive graph operations once to improve performance.
        Called during initialization to avoid repeated expensive calculations.
        """
        print("   📊 Computing descendants for all nodes...")
        descendants = {}
        for node_id in self.kg.nodes.keys():
            try:
                descendants[node_id] = list(nx.descendants(self.kg.graph, node_id))
            except:
                descendants[node_id] = []

        print("   📊 Computing betweenness centrality...")
        try:
            centrality = nx.betweenness_centrality(self.kg.graph)
        except:
            centrality = {node_id: 0.0 for node_id in self.kg.nodes.keys()}

        print("   📊 Computing shortest path lengths...")
        try:
            shortest_paths = dict(nx.all_pairs_shortest_path_length(self.kg.graph))
        except:
            shortest_paths = {}

        return {
            'descendants': descendants,
            'centrality': centrality,
            'shortest_paths': shortest_paths
        }


    def select_custom_mcqs(self, student_id: str,
                          custom_request: CustomStudyRequest) -> List[str]:
        """
        Main entry point for custom study MCQ selection.
        Implements the full custom study algorithm with all requested features.
        """
        student = self.student_manager.get_student(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        print(f"🎯 Starting custom study for {student_id}")
        print(f"   📊 Request: {custom_request.num_questions} questions")

        # Phase 1: Identify target nodes based on request
        target_nodes = self._identify_target_nodes(custom_request, student)
        if not target_nodes:
            print("❌ No target nodes identified")
            return []

        print(f"   🎯 Target nodes identified: {len(target_nodes)} nodes")

        # Phase 2: Prerequisite chain analysis
        if custom_request.prerequisite_testing:
            weak_prereqs = self._assess_prerequisite_chains(target_nodes, student, custom_request)
            if weak_prereqs:
                print(f"   ⚠️  Weak prerequisites found: {len(weak_prereqs)} topics")
                # Handle prerequisite questions first
                prereq_questions = self._handle_prerequisite_questions(
                    weak_prereqs, custom_request, student
                )
                if prereq_questions:
                    return prereq_questions

        # Phase 3: Main node selection using graph analysis
        selected_nodes = self._select_optimal_nodes_custom(
            target_nodes, custom_request, student
        )

        print(f"   ✅ Selected nodes for questions: {len(selected_nodes)} nodes")

        # Phase 4: MCQ selection with custom priorities
        selected_mcqs = self._select_mcqs_for_nodes(
            selected_nodes, custom_request, student
        )

        # Phase 5: Apply interleaving preference
        final_mcqs = self._apply_interleaving_sequence(
            selected_mcqs, custom_request.interleaving_preference
        )

        print(f"   🎉 Custom study complete: {len(final_mcqs)} questions selected")
        return final_mcqs

    def _identify_target_nodes(self, request: CustomStudyRequest,
                              student: StudentProfile) -> List[int]:
        """
        Phase 1: Identify target nodes based on student request.
        """
        candidate_nodes = set()

        # Step 1: Start with base set based on primary selection criteria
        if request.selected_nodes:
            # Direct node selection as starting point
            candidate_nodes = set(request.selected_nodes)
        elif request.selected_chapters:
            # Chapter-based selection as starting point
            candidate_nodes = set(self._get_nodes_in_chapters(request.selected_chapters))
        elif request.focus_weak_areas:
            # Weak area identification as starting point
            candidate_nodes = set(self._identify_weak_areas_by_centrality(student))
        elif request.review_due_tomorrow:
            # Tomorrow's due topics as starting point
            candidate_nodes = set(self._get_tomorrows_due_topics(student))
        else:
            # Default: all low mastery topics
            candidate_nodes = set([node_id for node_id, mastery in student.mastery_levels.items()
                                 if mastery < self.kg.config.get('algorithm_config.mastery_threshold', 0.7)])

        # Step 2: Apply additional filters if specified (intersection logic)

        # Apply chapter filter if specified and not already used as primary
        if request.selected_chapters and not any([request.selected_nodes]):
            chapter_nodes = set(self._get_nodes_in_chapters(request.selected_chapters))
            if candidate_nodes:
                candidate_nodes = candidate_nodes.intersection(chapter_nodes)

        # Apply weak area filter if specified and not already used as primary
        if request.focus_weak_areas and not any([request.selected_chapters, request.selected_nodes]):
            weak_nodes = set(self._identify_weak_areas_by_centrality(student))
            if candidate_nodes:
                candidate_nodes = candidate_nodes.intersection(weak_nodes)

        # Apply tomorrow due filter if specified and not already used as primary
        if request.review_due_tomorrow and not any([request.selected_chapters, request.selected_nodes, request.focus_weak_areas]):
            due_nodes = set(self._get_tomorrows_due_topics(student))
            if candidate_nodes:
                candidate_nodes = candidate_nodes.intersection(due_nodes)

        # Step 3: Filter by skill focus at node level (pre-filter before MCQ selection)
        if request.skill_focus:
            skill_relevant_nodes = self._filter_nodes_by_skill_availability(list(candidate_nodes), request.skill_focus)
            candidate_nodes = candidate_nodes.intersection(set(skill_relevant_nodes))

        return list(candidate_nodes)



    def _filter_nodes_by_skill_availability(self, nodes: List[int], target_skill: str) -> List[int]:
        """Filter nodes that have MCQs with significant focus on target skill"""
        skill_relevant_nodes = []
        skill_threshold = 0.4  # Minimum skill level required in MCQs

        for node_id in nodes:
            node_mcqs = self._get_mcqs_for_node(node_id)
            if self._node_has_skill_focus(node_mcqs, target_skill, skill_threshold):
                skill_relevant_nodes.append(node_id)
        return skill_relevant_nodes

    def _node_has_skill_focus(self, mcq_ids: List[str], target_skill: str, threshold: float) -> bool:
        """Check if node has MCQs with significant focus on target skill"""
        if not mcq_ids:
            return False

        skill_scores = []
        for mcq_id in mcq_ids:
            mcq_vector = self._get_or_create_optimized_mcq_vector(mcq_id)
            if mcq_vector and mcq_vector.difficulty_breakdown:
                skill_level = getattr(mcq_vector.difficulty_breakdown, target_skill, 0)
                skill_scores.append(skill_level)

        if not skill_scores:
            return False

        # Node qualifies if average skill level meets threshold
        avg_skill_level = sum(skill_scores) / len(skill_scores)
        return avg_skill_level >= threshold

    def _assess_prerequisite_chains(self, target_nodes: List[int],
                                   student: StudentProfile,
                                   request: CustomStudyRequest) -> List[int]:
        """
        Phase 2: Enhanced prerequisite assessment with BFS and computational limits.
        Identifies fundamental weaknesses in prerequisite chains.
        Uses batch processing to reduce graph traversals and improve performance.
        """

        # Batch prerequisite chain calculation for better performance
        prerequisite_chains = self.kg._get_prerequisite_chains_batch(
            target_nodes,
            max_depth=request.max_prerequisite_depth,
            max_nodes=request.max_prerequisite_nodes
        )

        weak_prerequisite_chains = []

        for target_node, prerequisite_chain in prerequisite_chains.items():
            # Check mastery along the chain
            for prereq_id in prerequisite_chain:
                mastery = student.mastery_levels.get(prereq_id, 0)
                centrality_weight = self._calculate_node_importance_cached(prereq_id)

                # Use precomputed shortest paths for distance calculation
                try:
                    distance = self._precomputed_metrics['shortest_paths'].get(prereq_id, {}).get(target_node, 1)
                except:
                    distance = 1

                weighted_threshold = (self.kg.config.get('algorithm_config.mastery_threshold', 0.7) *
                                    (1 + centrality_weight * 0.2) *
                                    (1 + 1/max(distance, 1) * 0.1))

                if mastery < weighted_threshold:
                    weak_prerequisite_chains.append(prereq_id)

        return list(set(weak_prerequisite_chains))







    def _select_optimal_nodes_custom(self, eligible_nodes: List[int],
                                   request: CustomStudyRequest,
                                   student: StudentProfile) -> List[int]:
        """
        Phase 3: Intelligent node selection using graph theory with computational efficiency.
        """
        # Computational efficiency check
        if len(eligible_nodes) > request.max_dfs_nodes:
            # Pre-filter by mastery and centrality before expensive operations
            eligible_nodes = self._pre_filter_by_mastery_and_centrality(
                eligible_nodes, student
            )[:request.max_dfs_nodes]

        # Calculate metrics for each node
        node_metrics = {}
        for node_id in eligible_nodes:
            node_metrics[node_id] = {
                'betweenness_centrality': self._get_cached_betweenness(node_id),
                'out_degree_centrality': self.kg.get_node_degree(node_id)['out_degree'],
                'mastery_level': student.mastery_levels.get(node_id, 0),
                'learning_impact_score': self._calculate_learning_impact(node_id, student)
            }

        # DFS skill clustering (only if skill_focus and computationally feasible)
        if request.skill_focus and len(eligible_nodes) <= request.max_dfs_nodes:
            skill_clusters = self._create_skill_clusters_dfs(eligible_nodes, request.skill_focus)
            return self._select_from_skill_clusters(skill_clusters, node_metrics, request)

        # Otherwise use balanced selection
        return self._select_balanced_efficient(node_metrics, request)

    def _calculate_learning_impact(self, node_id: int, student: StudentProfile) -> float:
        """
        Calculate learning impact score using precomputed graph metrics.
        Combines factors not already used in importance_bonus or centrality.
        """
        impact_score = 0.0

        # Factor 1: Mastery gap propagation
        # How much would improving this node close gaps in dependent topics
        try:
            dependents = self._precomputed_metrics['descendants'].get(node_id, [])
            mastery_gap_closure = 0
            for dependent_id in dependents:
                dependent_mastery = student.mastery_levels.get(dependent_id, 0)
                if dependent_mastery < self.config.mastery_threshold:
                    gap_size = self.kg.config.get('algorithm_config.mastery_threshold', 0.7) - dependent_mastery
                    mastery_gap_closure += gap_size
        except:
            mastery_gap_closure = 0

        # Factor 2: Skill diversity impact
        # How many different cognitive skills this node helps develop
        node_mcqs = self._get_mcqs_for_node(node_id)
        skill_diversity = self._calculate_skill_diversity_score(node_mcqs)

        # Factor 3: Learning sequence efficiency
        # How well positioned this node is in learning progressions
        sequence_efficiency = self._calculate_sequence_position_score(node_id)

        impact_score = (mastery_gap_closure * 0.4 +
                       skill_diversity * 0.3 +
                       sequence_efficiency * 0.3)

        return impact_score

    def _create_skill_clusters_dfs(self, nodes: List[int], target_skill: str) -> Dict[str, List[int]]:
        """
        DFS clustering with computational limits.
        Groups nodes by similar skill requirements.
        """
        clusters = {'high_skill': [], 'medium_skill': [], 'low_skill': []}
        visited = set()

        for start_node in nodes:
            if start_node in visited:
                continue

            # DFS with depth limit
            cluster_nodes = []
            self._dfs_skill_traverse(start_node, target_skill, visited, cluster_nodes, max_depth=3)

            # Categorize cluster by average skill requirement
            avg_skill_level = self._calculate_average_skill_level(cluster_nodes, target_skill)
            if avg_skill_level > 0.7:
                clusters['high_skill'].extend(cluster_nodes)
            elif avg_skill_level > 0.4:
                clusters['medium_skill'].extend(cluster_nodes)
            else:
                clusters['low_skill'].extend(cluster_nodes)

        return clusters

    def _select_mcqs_for_nodes(self, selected_nodes: List[int],
                              request: CustomStudyRequest,
                              student: StudentProfile) -> List[str]:
        """
        Phase 4: MCQ selection with custom priorities and skills focus.
        Excludes questions already completed today.
        """
        # Get eligible MCQs for selected nodes
        # Get eligible MCQs for selected nodes, excluding daily completed
        eligible_mcqs = self._get_available_mcqs_for_nodes(selected_nodes, student)

        if not eligible_mcqs:
            print("⚠️  No eligible MCQs found after filtering daily completed questions")
            return []
        print(f"   📚 Found {len(eligible_mcqs)} eligible MCQs (after daily filtering)")

        # Remove duplicates
        eligible_mcqs = list(set(eligible_mcqs))

        # Create topic priorities for coverage calculation
        topic_priorities = {node_id: 1.0 - student.mastery_levels.get(node_id, 0)
                           for node_id in selected_nodes}

        selected_mcqs = []
        simulated_mastery_levels = student.mastery_levels.copy()

        # Greedy selection with custom modifications
        for iteration in range(request.num_questions):
            if not topic_priorities:
                break

            best_mcq = None
            best_ratio = 0.0

            for mcq_id in eligible_mcqs:
                if mcq_id in selected_mcqs:
                    continue

                # Calculate custom coverage ratio
                ratio = self._calculate_custom_coverage_ratio(
                    mcq_id, topic_priorities, simulated_mastery_levels, student, request
                )

                if ratio > best_ratio:
                    best_ratio = ratio
                    best_mcq = mcq_id

            if best_mcq is None:
                break

            # Select the best MCQ
            selected_mcqs.append(best_mcq)

            # Update simulated mastery (simplified)
            mcq_vector = self._get_or_create_optimized_mcq_vector(best_mcq)
            if mcq_vector:
                for topic_id, weight in mcq_vector.subtopic_weights.items():
                    if topic_id in simulated_mastery_levels:
                        simulated_mastery_levels[topic_id] += weight * 0.1

                        # Remove topics that reach threshold
                        if simulated_mastery_levels[topic_id] >= self.kg.config.get('algorithm_config.mastery_threshold', 0.7):
                            topic_priorities.pop(topic_id, None)

        return selected_mcqs

    def _get_available_mcqs_for_nodes(self, selected_nodes: List[int], student: StudentProfile) -> List[str]:
        """
        Get MCQs for nodes, excluding those completed today.
        """
        eligible_mcqs = []
        today = datetime.now().date()

        for node_id in selected_nodes:
            node_mcqs = self._get_mcqs_for_node(node_id)

            # Filter out questions completed today
            for mcq_id in node_mcqs:
                if not self._is_completed_today(mcq_id, student, today):
                    eligible_mcqs.append(mcq_id)

        return eligible_mcqs

    def _is_completed_today(self, mcq_id: str, student: StudentProfile, today: datetime.date) -> bool:
        """Check if student completed this MCQ today"""
        # Check daily_completed attribute if it exists
        if hasattr(student, 'daily_completed'):
            today_str = today.isoformat()
            daily_completed = getattr(student, 'daily_completed', {})
            if today_str in daily_completed and mcq_id in daily_completed[today_str]:
                return True

        # Also check completed_questions with timestamp if available
        if hasattr(student, 'completed_questions'):
            for attempt in student.completed_questions:
                if (hasattr(attempt, 'mcq_id') and attempt.mcq_id == mcq_id and
                    hasattr(attempt, 'timestamp') and attempt.timestamp.date() == today):
                    return True

        return False

    def _calculate_custom_coverage_ratio(self, mcq_id: str,
                                       topic_priorities: Dict[int, float],
                                       simulated_mastery_levels: Dict[int, float],
                                       student: StudentProfile,
                                       request: CustomStudyRequest) -> float:
        """
        Calculate coverage ratio with custom study modifications.
        """
        # Get base ratio from existing algorithm
        base_ratio, coverage_info = self._calculate_coverage_to_cost_ratio(
            mcq_id, topic_priorities, simulated_mastery_levels, student
        )

        if base_ratio == 0:
            return 0.0

        modifiers = 1.0

        # Skills focus modifier with filtering
        if request.skill_focus:
            skill_modifier = self._calculate_skills_focus_modifier(mcq_id, student, request)
            if skill_modifier == 0:  # Below threshold - exclude question
                return 0.0
            modifiers *= skill_modifier

        # Difficulty preference modifier
        if request.difficulty_preference == "challenge":
            mcq_vector = self._get_or_create_optimized_mcq_vector(mcq_id)
            if mcq_vector:
                student_avg_mastery = np.mean(list(student.mastery_levels.values()))
                difficulty_gap = mcq_vector.difficulty - student_avg_mastery
                modifiers *= (1 + max(0, difficulty_gap) * 0.3)

        elif request.difficulty_preference == "simple":
            mcq_vector = self._get_or_create_optimized_mcq_vector(mcq_id)
            if mcq_vector:
                student_avg_mastery = np.mean(list(student.mastery_levels.values()))
                difficulty_gap = student_avg_mastery - mcq_vector.difficulty
                modifiers *= (1 + max(0, difficulty_gap) * 0.3)

        return base_ratio * modifiers

    def _calculate_skills_focus_modifier(self, mcq_id: str,
                                       student: StudentProfile,
                                       request: CustomStudyRequest) -> float:
        """
        Enhanced skills focus with filtering and weighting.
        """
        mcq_vector = self._get_or_create_optimized_mcq_vector(mcq_id)
        if not mcq_vector:
            return 0.0

        skill_focus = request.skill_focus

        # Adaptive threshold based on student's current skill level
        student_skill_level = student.ability_levels.get(skill_focus, 0.5)
        adaptive_threshold = max(0.4, min(0.8, student_skill_level + 0.1))
        # Get question's difficulty in focused skill
        question_skill_level = getattr(mcq_vector.difficulty_breakdown, skill_focus, 0)
        # Multi-tier filtering instead of binary threshold
        if question_skill_level < adaptive_threshold * 0.7:
            return 0.0  # Exclude entirely - too easy
        elif question_skill_level < adaptive_threshold:
            skill_modifier = 0.3  # Reduced weight - somewhat easy
        else:
            # Zone of proximal development bonus
            optimal_gap = 0.1 + (student_skill_level * 0.2)
            skill_gap = question_skill_level - student_skill_level

            if 0 < skill_gap <= optimal_gap:
                skill_modifier = 2.0  # Strong bonus for optimal challenge
            elif skill_gap > optimal_gap:
                skill_modifier = 1.0 + min(skill_gap * 0.5, 0.5)  # Moderate bonus for harder questions
            else:
                skill_modifier = 1.0  # Neutral for questions at student level

        # Reduce weighting on other skills to focus on target skill
        other_skills_penalty = self._calculate_other_skills_penalty(mcq_vector, skill_focus)

        return skill_modifier * (1 - other_skills_penalty * 0.3)


    def _apply_interleaving_sequence(self, selected_mcqs: List[str],
                                   interleaving_preference: float) -> List[str]:
        """
        Phase 5: Apply interleaving preference to question sequence.

        interleaving_preference:
        - 0.0: Fully clustered (all questions from same topic together)
        - 1.0: Fully interleaved (maximum mixing of topics)
        - 0.5: Balanced mixing
        """
        if not selected_mcqs or interleaving_preference == 0.5:
            return selected_mcqs  # Default ordering

        # Group MCQs by main topic
        topic_groups = {}
        for mcq_id in selected_mcqs:
            mcq_vector = self._get_or_create_optimized_mcq_vector(mcq_id)
            if mcq_vector:
                main_topic = mcq_vector.main_topic_index
                if main_topic not in topic_groups:
                    topic_groups[main_topic] = []
                topic_groups[main_topic].append(mcq_id)

        if interleaving_preference <= 0.1:
            # Fully clustered: all questions from same topic together
            sequenced_mcqs = []
            for topic_mcqs in topic_groups.values():
                sequenced_mcqs.extend(topic_mcqs)
            return sequenced_mcqs

        elif interleaving_preference >= 0.9:
            # Fully interleaved: round-robin through topics
            sequenced_mcqs = []
            topic_iterators = [iter(mcqs) for mcqs in topic_groups.values()]

            while topic_iterators:
                for i, iterator in enumerate(topic_iterators[:]):
                    try:
                        sequenced_mcqs.append(next(iterator))
                    except StopIteration:
                        topic_iterators.remove(iterator)

            return sequenced_mcqs

        else:
            # Balanced interleaving based on preference
            # Randomly shuffle with bias toward clustering/interleaving
            sequenced_mcqs = selected_mcqs.copy()

            # Apply shuffle with clustering bias
            cluster_size = max(1, int((1.0 - interleaving_preference) * 3))
            random.shuffle(sequenced_mcqs)

            return sequenced_mcqs

    # Helper methods
    def _get_nodes_in_chapters(self, chapters: List[str]) -> List[int]:
        """Get all node IDs that belong to specified chapters."""
        nodes = []
        for node_id, node in self.kg.nodes.items():
            if node.chapter in chapters:
                nodes.append(node_id)
        return nodes

    def _identify_weak_areas_by_centrality(self, student: StudentProfile) -> List[int]:
        """Identify weak areas using centrality analysis."""
        weak_nodes = []
        for node_id, mastery in student.mastery_levels.items():
            if mastery < self.kg.config.get('algorithm_config.mastery_threshold', 0.7):
                centrality = self._get_cached_betweenness(node_id)
                if centrality > 0.1:  # High centrality nodes
                    weak_nodes.append(node_id)
        return weak_nodes


    def _get_tomorrows_due_topics(self, student: StudentProfile) -> List[int]:
        """
        Get topics that will be due tomorrow using FSRS predictions.
        Falls back to mastery-based approach if FSRS not available.
        """
        # Try to use FSRS if available
        if (hasattr(self, 'bkt_system') and self.bkt_system and
            hasattr(self.bkt_system, 'fsrs_forgetting') and self.bkt_system.fsrs_forgetting):

            return self._get_tomorrows_due_topics_fsrs(student)

        # Fallback to mastery-based approach
        return self._get_tomorrows_due_topics_fallback(student)

    def _get_tomorrows_due_topics_fsrs(self, student: StudentProfile) -> List[int]:
        """Get topics that will be due tomorrow using FSRS predictions"""
        from datetime import timedelta

        tomorrow = datetime.now() + timedelta(days=1)
        due_topics = []

        print("   🔮 Using FSRS to predict tomorrow's due topics...")

        for topic_id in student.mastery_levels.keys():
            try:
                # Get FSRS memory components
                memory_components = self.bkt_system.fsrs_forgetting.get_memory_components(
                    student.id if hasattr(student, 'id') else 'unknown_student',
                    topic_id
                )

                # Calculate predicted retrievability tomorrow
                predicted_retrievability = self.bkt_system.fsrs_forgetting.calculate_retrievability(
                    memory_components, tomorrow
                )

                # Topic is due if retrievability drops below threshold
                retrievability_threshold = self.kg.config.get('bkt_config.fsrs_retrievability_threshold')
                if predicted_retrievability < retrievability_threshold:
                    due_topics.append(topic_id)

            except Exception as e:
                # If FSRS calculation fails for this topic, skip it
                print(f"   ⚠️  FSRS calculation failed for topic {topic_id}: {e}")
                continue

        print(f"   📅 FSRS predicted {len(due_topics)} topics due tomorrow")
        return due_topics

    def _get_tomorrows_due_topics_fallback(self, student: StudentProfile) -> List[int]:
        """
        Fallback method when FSRS is not available.
        Returns topics with mastery just above threshold (likely to decay soon).
        """
        print("   📅 Using fallback method for tomorrow's due topics...")
        due_topics = []

        # Topics with mastery slightly above threshold are likely to become due soon
        for node_id, mastery in student.mastery_levels.items():
            if self.kg.config.get('algorithm_config.mastery_threshold', 0.7)<= mastery <= self.kg.config.get('algorithm_config.mastery_threshold', 0.7) + 0.1:
                due_topics.append(node_id)

        print(f"   📅 Fallback method found {len(due_topics)} potentially due topics")
        return due_topics

    def _get_cached_betweenness(self, node_id: int) -> float:
        """Get cached betweenness centrality."""
        if node_id not in self._centrality_cache:
            try:
                centrality = nx.betweenness_centrality(self.kg.graph)
                self._centrality_cache.update(centrality)
            except:
                self._centrality_cache[node_id] = 0.0
        return self._centrality_cache.get(node_id, 0.0)

    def _calculate_node_importance_cached(self, node_id: int) -> float:
        """Cached version of node importance calculation."""
        # Use existing importance calculation from parent class
        return self.kg.get_node_degree(node_id)['out_degree'] / 10.0  # Normalize

    def _get_mcqs_for_node(self, node_id: int) -> List[str]:
        """Get all MCQ IDs that test a specific node."""
        mcq_ids = []
        if hasattr(self.kg, 'ultra_loader'):
            mcq_ids = self.kg.ultra_loader.get_mcq_ids_for_due_topics([node_id])
        else:
            # Fallback for regular loading
            for mcq_id, mcq in self.kg.mcqs.items():
                if mcq.main_topic_index == node_id or node_id in mcq.subtopic_weights:
                    mcq_ids.append(mcq_id)
        return mcq_ids

    # Additional helper methods for completeness
    def _pre_filter_by_mastery_and_centrality(self, nodes: List[int],
                                             student: StudentProfile) -> List[int]:
        """Pre-filter nodes by mastery and centrality before expensive operations."""
        scored_nodes = []
        for node_id in nodes:
            mastery = student.mastery_levels.get(node_id, 0)
            centrality = self._get_cached_betweenness(node_id)
            score = (1 - mastery) + centrality  # Lower mastery + higher centrality = higher score
            scored_nodes.append((node_id, score))

        scored_nodes.sort(key=lambda x: x[1], reverse=True)
        return [node_id for node_id, score in scored_nodes]

    def _calculate_skill_diversity_score(self, mcq_ids: List[str]) -> float:
        """Calculate how diverse the cognitive skills are for a set of MCQs."""
        if not mcq_ids:
            return 0.0

        skill_counts = {}
        for mcq_id in mcq_ids:
            mcq_vector = self._get_or_create_optimized_mcq_vector(mcq_id)
            if mcq_vector and mcq_vector.difficulty_breakdown:
                breakdown = mcq_vector.difficulty_breakdown
                for skill in ['conceptual_understanding', 'procedural_fluency', 'problem_solving',
                             'mathematical_communication', 'memory', 'spatial_reasoning']:
                    skill_level = getattr(breakdown, skill, 0)
                    if skill_level > 0.3:  # Significant skill requirement
                        skill_counts[skill] = skill_counts.get(skill, 0) + 1

        # Diversity = number of different skills involved
        return len(skill_counts) / 6.0  # Normalize by max possible skills

    def _calculate_sequence_position_score(self, node_id: int) -> float:
        """Calculate how well positioned a node is in learning sequences."""
        try:
            # Use precomputed graph structure instead of expensive NetworkX calls
            predecessors = 0
            successors = 0

            # Count predecessors (nodes that depend on this node)
            for other_node_id, deps in self._precomputed_metrics['descendants'].items():
                if node_id in deps:
                    predecessors += 1

            # Count successors (nodes this node depends on - direct dependencies)
            node = self.kg.get_node_by_index(node_id)
            if node:
                successors = len(node.dependencies)

            # Normalize and combine
            return (predecessors + successors) / (len(self.kg.nodes) * 0.1)
        except:
            return 0.0

    def _dfs_skill_traverse(self, start_node: int, target_skill: str,
                           visited: Set[int], cluster_nodes: List[int],
                           max_depth: int = 3, current_depth: int = 0) -> None:
        """DFS traversal for skill clustering with depth limit."""
        if current_depth >= max_depth or start_node in visited:
            return

        visited.add(start_node)

        # Check if this node has significant requirement for target skill
        node_mcqs = self._get_mcqs_for_node(start_node)
        avg_skill_level = self._calculate_average_skill_level([start_node], target_skill)

        if avg_skill_level > 0.3:  # Significant skill requirement
            cluster_nodes.append(start_node)

        # Continue DFS to connected nodes
        try:
            for neighbor in self.kg.graph.neighbors(start_node):
                self._dfs_skill_traverse(neighbor, target_skill, visited, cluster_nodes,
                                       max_depth, current_depth + 1)
        except:
            pass  # Handle graph traversal errors gracefully

    def _calculate_average_skill_level(self, node_ids: List[int], skill: str) -> float:
        """Calculate average skill level for a set of nodes."""
        total_skill = 0.0
        count = 0

        for node_id in node_ids:
            node_mcqs = self._get_mcqs_for_node(node_id)
            for mcq_id in node_mcqs:
                mcq_vector = self._get_or_create_optimized_mcq_vector(mcq_id)
                if mcq_vector and mcq_vector.difficulty_breakdown:
                    skill_level = getattr(mcq_vector.difficulty_breakdown, skill, 0)
                    total_skill += skill_level
                    count += 1

        return total_skill / count if count > 0 else 0.0

    def _select_from_skill_clusters(self, clusters: Dict[str, List[int]],
                                   node_metrics: Dict[int, Dict],
                                   request: CustomStudyRequest) -> List[int]:
        """Select nodes from skill clusters based on student needs."""
        selected_nodes = []

        # Prioritize high skill nodes for skill focus
        if request.skill_focus:
            high_skill_nodes = clusters.get('high_skill', [])
            selected_nodes.extend(high_skill_nodes[:request.num_questions//2])

        # Add medium skill nodes for balance
        medium_skill_nodes = clusters.get('medium_skill', [])
        remaining_slots = request.num_questions - len(selected_nodes)
        selected_nodes.extend(medium_skill_nodes[:remaining_slots])

        return selected_nodes

    def _select_balanced_efficient(self, node_metrics: Dict[int, Dict],
                                  request: CustomStudyRequest) -> List[int]:
        """Efficient balanced selection when DFS clustering isn't used."""
        # Score nodes by combined metrics
        scored_nodes = []
        for node_id, metrics in node_metrics.items():
            score = (
                (1 - metrics['mastery_level']) * 0.4 +  # Prioritize low mastery
                metrics['betweenness_centrality'] * 0.3 +  # Important nodes
                metrics['learning_impact_score'] * 0.3  # High impact nodes
            )
            scored_nodes.append((node_id, score))

        # Sort by score and take top nodes
        scored_nodes.sort(key=lambda x: x[1], reverse=True)
        return [node_id for node_id, score in scored_nodes[:request.num_questions]]

    def _calculate_other_skills_penalty(self, mcq_vector: OptimizedMCQVector,
                                       focus_skill: str) -> float:
        """Calculate penalty for questions that test non-focused skills heavily."""
        if not mcq_vector.difficulty_breakdown:
            return 0.0

        other_skills_total = 0.0
        skill_count = 0

        for skill in ['conceptual_understanding', 'procedural_fluency', 'problem_solving',
                     'mathematical_communication', 'memory', 'spatial_reasoning']:
            if skill != focus_skill:
                skill_level = getattr(mcq_vector.difficulty_breakdown, skill, 0)
                other_skills_total += skill_level
                skill_count += 1

        return other_skills_total / skill_count if skill_count > 0 else 0.0

    def _handle_prerequisite_questions(self, weak_prereqs: List[int],
                                     request: CustomStudyRequest,
                                     student: StudentProfile) -> List[str]:
        """Handle questions for weak prerequisites."""
        # Create a focused request for prerequisites
        prereq_request = CustomStudyRequest(
            selected_nodes=weak_prereqs,
            num_questions=min(request.num_questions, len(weak_prereqs) * 2),
            difficulty_preference="simple",  # Start with simpler questions
            prerequisite_testing=False,  # Avoid infinite recursion
            interleaving_preference=0.3  # Slight clustering for prerequisites
        )

        # Select prerequisite nodes (most important/weakest first)
        prereq_nodes = self._select_optimal_nodes_custom(weak_prereqs, prereq_request, student)

        # Get MCQs for prerequisite nodes
        return self._select_mcqs_for_nodes(prereq_nodes, prereq_request, student)


# Integration helper function
def create_custom_study_session(knowledge_graph: KnowledgeGraph,
                               student_manager: StudentManager,
                               student_id: str,
                               bkt_system=None,
                               **kwargs) -> List[str]:
    """
    Convenience function to create a custom study session.

    Usage example:
    selected_mcqs = create_custom_study_session(
        kg, student_manager, "student_123", bkt_system,
        selected_chapters=["algebra"],
        num_questions=10,
        skill_focus="procedural_fluency",
        difficulty_preference="challenge"
    )
    """
    custom_request = CustomStudyRequest(**kwargs)
    scheduler = CustomStudyScheduler(knowledge_graph, student_manager, bkt_system)
    return scheduler.select_custom_mcqs(student_id, custom_request)


kg = KnowledgeGraph('_static/kg_new.json', '_static/computed_mcqs_breakdown.json', '_static/config.json')
student_manager = StudentManager(kg.config)
mcq_scheduler = MCQScheduler(kg, student_manager)  # Create scheduler first
bkt_system = BayesianKnowledgeTracing(kg, student_manager, scheduler=mcq_scheduler)
# Create test student with some mastery levels
student_id = "test_student"
student = student_manager.create_student(student_id)
import random
# Set initial mastery levels if you want
for topic_idx in kg.get_all_indexes():
    mastery = random.uniform(0.1, 0.6)
    student.mastery_levels[topic_idx] = mastery
    student.confidence_levels[topic_idx] = mastery * 0.8
    student.studied_topics[topic_idx] = True
# Test the new system
selected_mcqs = create_custom_study_session(
    kg, student_manager, "test_student", bkt_system,
    selected_chapters=["algebra"], difficulty_preference= "simple", num_questions=18
)
print(f"Selected: {selected_mcqs}")
for mcq_id in selected_mcqs:
    mcq = kg.get_mcq_safely(mcq_id, need_full_text=True)
    print(mcq.question_text,)
