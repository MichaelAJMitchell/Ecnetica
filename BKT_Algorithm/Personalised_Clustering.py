
"""
Personalized Clustered Bayesian Knowledge Tracing (PCBKT) Implementation

This implementation discovers student learning patterns and assigns personalized
BKT parameters based on cluster membership.
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json


class PCBKTSystem:
    """
    PCBKT system for discovering student clusters and assigning
    personalized BKT parameters.
    """
    
    def __init__(self, n_clusters=3, use_svd=False, svd_threshold=0.95):
        self.n_clusters = n_clusters
        self.use_svd = use_svd
        self.svd_threshold = svd_threshold
        
        # Will be populated during training
        self.kmeans_model = None
        self.cluster_bkt_parameters = {}
        self.cluster_avg_capabilities = {}
        self.skills = []
        
        # SVD components (if used)
        self.svd_components = None
        self.n_components = None
        
    def build_capability_matrix(self, students_data, skills):
        """
        Build Student Capability Matrix
        
        Convert student performance data into a structured matrix where
        each row represents a student and each column represents a skill.
        
        Args:
            students_data: List of student objects with performance history
            skills: List of skill names/IDs from knowledge graph
        """        
        self.skills = skills
        capability_matrix = []
        
        for student in students_data:
            student_capabilities = []
            
            for skill in skills:
                # Calculate capability as success rate
                correct = self.count_correct_answers(student, skill)
                total = self.count_total_attempts(student, skill)
                
                # Convert to capability score (0.0 to 1.0)
                if total > 0:
                    capability = correct / total
                else:
                    # Default for untested skills - conservative estimate
                    capability = 0.3
                
                student_capabilities.append(capability)
            
            capability_matrix.append(student_capabilities)
        
        capability_matrix = np.array(capability_matrix)
        
        print(f" Built matrix: {capability_matrix.shape[0]} students × {capability_matrix.shape[1]} skills")
        print(f" Capability range: {capability_matrix.min():.2f} to {capability_matrix.max():.2f}")
        
        return capability_matrix
    
    def apply_svd_if_needed(self, capability_matrix):
        """
        SVD Dimensionality Reduction
        
        If we have many skills (>10), reduce dimensionality and removes noise to find
        the main patterns in how students differ.
        """
                
        # Perform SVD decomposition
        U, sigma, VT = np.linalg.svd(capability_matrix, full_matrices=False)
        
        # Determine how many components to keep
        explained_variance = (sigma ** 2) / np.sum(sigma ** 2)
        cumulative_variance = np.cumsum(explained_variance)
        self.n_components = np.argmax(cumulative_variance >= self.svd_threshold) + 1
        
        # Keep only the most important patterns
        reduced_data = U[:, :self.n_components]
        
        # Store SVD components for new student assignment
        self.svd_components = {
            'U': U,
            'sigma': sigma,
            'VT': VT,
            'n_components': self.n_components
        }
        
        print(f"Reduced from {capability_matrix.shape[1]} skills to {self.n_components} patterns")
        print(f"Patterns explain {cumulative_variance[self.n_components-1]:.1%} of variance")
        
        return reduced_data
    
    def discover_clusters(self, processed_data):
        """
        Discover Student Clusters
        Clustering finds the "types" of learners in our data
        
        Algorithm: K-means clustering finds k=3 groups by:
        1. Placing 3 random "cluster centres" in capability space
        2. Assigning each student to nearest center
        3. Moving centres to average of assigned students
        4. Repeating until centres stop moving
        """        
        # Train K-means clustering model
        self.kmeans_model = KMeans(n_clusters=self.n_clusters, random_state=42)
        cluster_labels = self.kmeans_model.fit_predict(processed_data)
        
        # Evaluate clustering quality
        silhouette = silhouette_score(processed_data, cluster_labels)
        
        # Analyze cluster sizes
        unique, counts = np.unique(cluster_labels, return_counts=True)
        cluster_sizes = dict(zip(unique, counts))
        
        print(f"   Discovered {self.n_clusters} clusters")
        print(f"   Clustering quality (silhouette): {silhouette:.3f}")
        print(f"   Cluster sizes: {cluster_sizes}")
    
        return cluster_labels
    
    def calculate_cluster_parameters(self, capability_matrix, cluster_labels):
        """
        Calculate BKT Parameters for Each Cluster
        
        Convert cluster membership into actual BKT parameters
        
        Method:
        - Find the "average student" in each cluster
        - Convert their capabilities into appropriate BKT parameters
        - Store these for assigning to new students
        """
        
        for cluster_id in range(self.n_clusters):
            # Find all students in this cluster
            cluster_students = [i for i, c in enumerate(cluster_labels) if c == cluster_id]
            
            # Calculate average capabilities for this cluster
            cluster_capabilities = [capability_matrix[i] for i in cluster_students]
            cluster_avg_capability = np.mean(cluster_capabilities, axis=0)
            
            # Store cluster profile
            self.cluster_avg_capabilities[cluster_id] = cluster_avg_capability
            
            # Convert to BKT parameters
            overall_capability = np.mean(cluster_avg_capability)
            
            # Parameter mapping formulas (these can be tuned)
            bkt_params = {
                'prior_knowledge': 0.1 + overall_capability * 0.6,  # Range: 0.1 to 0.7
                'learning_rate': 0.2 + overall_capability * 0.4,    # Range: 0.2 to 0.6
                'slip_rate': 0.3 * (1 - overall_capability),        # Higher capability = fewer slips
                'guess_rate': 0.1 + (1 - overall_capability) * 0.2  # Lower capability = more guessing
            }
            
            self.cluster_bkt_parameters[cluster_id] = bkt_params
            
            print(f"Cluster {cluster_id} ({len(cluster_students)} students):")
            print(f"Average capability: {overall_capability:.3f}")
            print(f"BKT params: P(L₀)={bkt_params['prior_knowledge']:.3f}, "
                  f"P(T)={bkt_params['learning_rate']:.3f}, "
                  f"P(S)={bkt_params['slip_rate']:.3f}, "
                  f"P(G)={bkt_params['guess_rate']:.3f}")
    
    def train_clusters(self, students_data, skills):
        """
        Complete training pipeline for PCBKT system
        
        This uses all the steps
        """        
        # Step 1: Build capability matrix from student data
        capability_matrix = self.build_capability_matrix(students_data, skills)
        
        # Step 2: Apply SVD
        processed_data = self.apply_svd_if_needed(capability_matrix)
        
        # Step 3: Discover clusters
        cluster_labels = self.discover_clusters(processed_data)
        
        # Step 4: Calculate BKT parameters
        self.calculate_cluster_parameters(capability_matrix, cluster_labels)
        
        return cluster_labels
    
    def assign_new_student(self, diagnostic_results):
        """
        Assign New Student to Cluster
        
        When a new student arrives, figure out which cluster (learning type)
        they belong to based on a short diagnostic assessment.
        
        Method:
        1. Convert diagnostic results to capability estimates
        2. Transform using same processing as training (SVD if used)
        3. Find closest cluster using trained model
        4. Return that cluster's BKT parameters
        """
        if self.kmeans_model is None:
            raise ValueError("Must train clusters first!")
                
        # Convert diagnostic to capability vector
        new_capabilities = self.diagnostic_to_capabilities(diagnostic_results)
        
        # Apply same preprocessing as training
        if self.use_svd and self.svd_components is not None:
            # Project new student into same reduced space used for training
            U = self.svd_components['U']
            sigma = self.svd_components['sigma']
            VT = self.svd_components['VT']
            
            # This is complex - for now, use direct assignment
            processed_capabilities = new_capabilities
        else:
            processed_capabilities = new_capabilities
        
        # Assign to closest cluster
        cluster_id = self.kmeans_model.predict([processed_capabilities])[0]
        
        # Get BKT parameters for this cluster
        bkt_params = self.cluster_bkt_parameters[cluster_id]
        
        # Calculate confidence in assignment
        confidence = self.calculate_assignment_confidence(processed_capabilities, cluster_id)
        
        result = {
            'assigned_cluster': cluster_id,
            'estimated_capabilities': new_capabilities,
            'bkt_parameters': bkt_params,
            'assignment_confidence': confidence
        }
        
        print(f"   Assigned to cluster {cluster_id}")
        print(f"   Confidence: {confidence:.3f}")
        print(f"   BKT params: P(L₀)={bkt_params['prior_knowledge']:.3f}")
        
        return result
    
    def diagnostic_to_capabilities(self, diagnostic_results):
        """
        Convert diagnostic assessment results to capability estimates
        """
        capabilities = []
        
        for skill in self.skills:
            if skill in diagnostic_results:
                correct = diagnostic_results[skill]['correct']
                total = diagnostic_results[skill]['total']
                capability = correct / total if total > 0 else 0.3
            else:
                # No diagnostic data for this skill
                capability = 0.3  # Conservative default
                # TODO: Could use knowledge graph to infer from related skills
            
            capabilities.append(capability)
        
        return capabilities
    
    def calculate_assignment_confidence(self, capabilities, assigned_cluster):
        """
        Calculate confidence in cluster assignment
        
        Higher confidence = student is clearly similar to their assigned cluster
        Lower confidence = student is between clusters (ambiguous assignment)
        """
        cluster_centers = self.kmeans_model.cluster_centers_
        
        # Distance to assigned cluster
        assigned_distance = np.linalg.norm(
            np.array(capabilities) - cluster_centers[assigned_cluster]
        )
        
        # Distance to all clusters
        all_distances = [
            np.linalg.norm(np.array(capabilities) - center)
            for center in cluster_centers
        ]
        
        # Confidence = how much closer to assigned vs next closest
        sorted_distances = sorted(all_distances)
        if len(sorted_distances) > 1:
            confidence = sorted_distances[1] / (sorted_distances[0] + 0.01)
        else:
            confidence = 1.0
        
        return min(confidence, 1.0)
    

#This measures how good our cluster choices are but not how good our actual parameters are
#The next step after this is to then test how accurate our parameter assignment is


