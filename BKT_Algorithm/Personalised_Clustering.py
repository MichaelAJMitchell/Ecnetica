"""
Graph Laplacian Enhanced Personalized Clustered Bayesian Knowledge Tracing (GL-PCBKT)

This enhanced implementation uses graph Laplacian regularization to make SVD
dimensionality reduction aware of topic connection weights from the directed knowledge graph.
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.linalg import eigh
from scipy.sparse import csgraph
import json


class GraphLaplacianPCBKT:
    """
    Enhanced PCBKT system that incorporates knowledge graph structure
    into dimensionality reduction via graph Laplacian regularization.
    """
    
    def __init__(self, n_clusters=3, use_graph_laplacian=True, 
                 laplacian_weight=0.5, svd_threshold=0.95):
        self.n_clusters = n_clusters
        self.use_graph_laplacian = use_graph_laplacian
        self.laplacian_weight = laplacian_weight  # Balance between data and graph structure
        self.svd_threshold = svd_threshold
        
        # Will be populated during training
        self.kmeans_model = None
        self.cluster_bkt_parameters = {}
        self.cluster_avg_capabilities = {}
        self.skills = []
        self.skill_to_index = {}  # Map skill names to matrix indices
        
        # Graph Laplacian components
        self.graph_laplacian = None
        self.graph_aware_components = None
        self.n_components = None
        
        # Knowledge graph reference
        self.knowledge_graph = None
        
    def set_knowledge_graph(self, knowledge_graph):
        """Set reference to knowledge graph for accessing adjacency matrix"""
        self.knowledge_graph = knowledge_graph
    
    def build_capability_matrix(self, students_data, skills):
        """
        Build Student Capability Matrix with skill indexing
        """        
        self.skills = skills
        self.skill_to_index = {skill: idx for idx, skill in enumerate(skills)}
        capability_matrix = []
        
        for student in students_data:
            student_capabilities = []
            
            for skill in skills:
                # Calculate capability as success rate
                correct = self.count_correct_answers(student, skill)
                total = self.count_total_attempts(student, skill)
                
                # Convert to capability score (0.0 to 1.0)
                # Which we take as just being their percentage of correct answers
                if total > 0:
                    capability = correct / total
                else:
                    # Default for untested skills - conservative estimate
                    capability = 0.3
                
                student_capabilities.append(capability)
            
            capability_matrix.append(student_capabilities)
        
        capability_matrix = np.array(capability_matrix)
        
        print(f"Built matrix: {capability_matrix.shape[0]} students × {capability_matrix.shape[1]} skills")
        print(f"Capability range: {capability_matrix.min():.2f} to {capability_matrix.max():.2f}")
        
        return capability_matrix
    
    def build_graph_laplacian(self):
        """
        Build Graph Laplacian from knowledge graph adjacency matrix
        
        The Laplacian captures the structure of topic relationships:
        - L = D - A (where D is degree matrix, A is adjacency matrix)
        - For directed graphs, we use the symmetrized version: (A + A^T) / 2
        """
        if self.knowledge_graph is None:
            raise ValueError("Knowledge graph must be set before building Laplacian")
        
        # Get adjacency matrix from knowledge graph
        adjacency_full = self.knowledge_graph.get_adjacency_matrix()
        
        if adjacency_full.size == 0:
            print("Empty adjacency matrix, using identity for Laplacian")
            n_skills = len(self.skills)
            self.graph_laplacian = np.eye(n_skills)
            return self.graph_laplacian
        
        # Map skills to knowledge graph indices
        n_skills = len(self.skills)
        adjacency_filtered = np.zeros((n_skills, n_skills))
        
        skill_indices = []
        for skill in self.skills:
            # Find corresponding index in knowledge graph
            if isinstance(skill, int):
                skill_indices.append(skill)
            else:
                # If skills are topic names, find their indices
                topic_index = self.knowledge_graph.topic_to_index.get(skill, -1)
                skill_indices.append(topic_index)
        
        # Extract relevant submatrix for our skills
        valid_indices = [i for i, idx in enumerate(skill_indices) if 0 <= idx < adjacency_full.shape[0]]
        kg_indices = [skill_indices[i] for i in valid_indices]
        
        if len(kg_indices) > 0:
            # Extract submatrix for valid skills
            sub_adjacency = adjacency_full[np.ix_(kg_indices, kg_indices)]
            
            # Fill in the filtered adjacency matrix
            for i, valid_i in enumerate(valid_indices):
                for j, valid_j in enumerate(valid_indices):
                    adjacency_filtered[valid_i, valid_j] = sub_adjacency[i, j]
        
        # Symmetrize the directed adjacency matrix
        adjacency_sym = (adjacency_filtered + adjacency_filtered.T) / 2
        
        # Compute degree matrix
        degrees = np.sum(adjacency_sym, axis=1)
        degree_matrix = np.diag(degrees)
        
        # Compute normalized Laplacian: L = I - D^(-1/2) * A * D^(-1/2)
        # This handles disconnected components better
        with np.errstate(divide='ignore', invalid='ignore'):
            inv_sqrt_degrees = np.power(degrees, -0.5)
            inv_sqrt_degrees[np.isinf(inv_sqrt_degrees)] = 0
            inv_sqrt_degree_matrix = np.diag(inv_sqrt_degrees)
        
        normalized_adjacency = inv_sqrt_degree_matrix @ adjacency_sym @ inv_sqrt_degree_matrix
        self.graph_laplacian = np.eye(n_skills) - normalized_adjacency
        
        # Ensure positive semi-definite (numerical stability)
        eigenvals = np.linalg.eigvals(self.graph_laplacian)
        min_eigenval = np.min(eigenvals)
        if min_eigenval < -1e-10:  # Allow small numerical errors
            self.graph_laplacian += (-min_eigenval + 1e-8) * np.eye(n_skills)
        
        print(f" Built graph Laplacian: {self.graph_laplacian.shape}")
        print(f" Eigenvalue range: {np.min(eigenvals):.6f} to {np.max(eigenvals):.6f}")
        print(f" Non-zero connections: {np.count_nonzero(adjacency_sym)}")
        
        return self.graph_laplacian
    
    def apply_graph_laplacian_svd(self, capability_matrix):
        """
        Apply Graph Laplacian regularized dimensionality reduction
        
        This finds low-dimensional representations that preserve both:
        1. Variance in student capabilities (like regular SVD)
        2. Graph structure relationships between topics
        
        Method: Solve generalized eigenvalue problem:
        X^T X v = λ (X^T X + α L) v
        
        Where:
        - X is capability matrix (students × skills)
        - L is graph Laplacian
        - α is regularization weight
        - v are the graph-aware principal components
        """
        if not self.use_graph_laplacian:
            return self.apply_regular_svd(capability_matrix)
        
        # Build graph Laplacian
        self.build_graph_laplacian()
        
        # Center the data
        capability_centered = capability_matrix - np.mean(capability_matrix, axis=0)
        
        # Compute covariance matrix: X^T X
        covariance_matrix = capability_centered.T @ capability_centered
        
        # Add graph Laplacian regularization: X^T X + α L
        regularized_matrix = covariance_matrix + self.laplacian_weight * self.graph_laplacian
        
        # Solve generalized eigenvalue problem
        # We want: covariance_matrix @ v = λ @ regularized_matrix @ v
        try:
            eigenvals, eigenvecs = eigh(covariance_matrix, regularized_matrix)
            
            # Sort by eigenvalues (descending)
            sorted_indices = np.argsort(eigenvals)[::-1]
            eigenvals = eigenvals[sorted_indices]
            eigenvecs = eigenvecs[:, sorted_indices]
            
        except np.linalg.LinAlgError:
            print(" Generalized eigenvalue decomposition failed, using regular SVD")
            return self.apply_regular_svd(capability_matrix)
        
        # Determine number of components to keep
        # Use eigenvalue proportion as proxy for explained variance
        total_eigenval = np.sum(np.maximum(eigenvals, 0))  # Only positive eigenvalues
        if total_eigenval > 0:
            explained_variance = np.maximum(eigenvals, 0) / total_eigenval
            cumulative_variance = np.cumsum(explained_variance)
            self.n_components = np.argmax(cumulative_variance >= self.svd_threshold) + 1
        else:
            self.n_components = min(3, len(eigenvals))  # Fallback
        
        # Keep top components
        self.n_components = min(self.n_components, capability_matrix.shape[1])
        self.graph_aware_components = eigenvecs[:, :self.n_components]
        
        # Project data to reduced space
        reduced_data = capability_centered @ self.graph_aware_components
        
        print(f" Graph-aware reduction: {capability_matrix.shape[1]} → {self.n_components} dimensions")
        print(f" Captured variance: {cumulative_variance[self.n_components-1]:.1%}")
        print(f" Laplacian weight: {self.laplacian_weight}")
        
        return reduced_data
    
    def apply_regular_svd(self, capability_matrix):
        """regular SVD if graph Laplacian fails"""
        U, sigma, VT = np.linalg.svd(capability_matrix, full_matrices=False)
        
        explained_variance = (sigma ** 2) / np.sum(sigma ** 2)
        cumulative_variance = np.cumsum(explained_variance)
        self.n_components = np.argmax(cumulative_variance >= self.svd_threshold) + 1
        
        reduced_data = U[:, :self.n_components]
        self.graph_aware_components = VT[:self.n_components].T
        
        print(f"Regular SVD: {capability_matrix.shape[1]} → {self.n_components} dimensions")
        print(f"Explained variance: {cumulative_variance[self.n_components-1]:.1%}")
        
        return reduced_data
    
    def discover_clusters(self, processed_data):
        """
        Discover Student Clusters in graph-aware reduced space
        """        
        # Train K-means clustering model
        self.kmeans_model = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        cluster_labels = self.kmeans_model.fit_predict(processed_data)
        
        # Evaluate clustering quality
        if len(np.unique(cluster_labels)) > 1:
            silhouette = silhouette_score(processed_data, cluster_labels)
        else:
            silhouette = 0.0
        
        # Analyze cluster sizes
        unique, counts = np.unique(cluster_labels, return_counts=True)
        cluster_sizes = dict(zip(unique, counts))
        
        print(f" Discovered {self.n_clusters} clusters")
        print(f" Clustering quality (silhouette): {silhouette:.3f}")
        print(f" Cluster sizes: {cluster_sizes}")
    
        return cluster_labels
    
    def calculate_cluster_parameters(self, capability_matrix, cluster_labels):
        """
        Calculate BKT Parameters for Each Cluster
        
        Enhanced with graph-aware insights
        """
        
        for cluster_id in range(self.n_clusters):
            # Find all students in this cluster
            cluster_students = [i for i, c in enumerate(cluster_labels) if c == cluster_id]
            
            if len(cluster_students) == 0:
                continue
            
            # Calculate average capabilities for this cluster
            cluster_capabilities = [capability_matrix[i] for i in cluster_students]
            cluster_avg_capability = np.mean(cluster_capabilities, axis=0)
            
            # Store cluster profile
            self.cluster_avg_capabilities[cluster_id] = cluster_avg_capability
            
            # Enhanced parameter calculation using graph structure
            overall_capability = np.mean(cluster_avg_capability)
            
            # Calculate graph-aware capability variance
            if self.use_graph_laplacian and self.graph_laplacian is not None:
                # Measure how much capability varies along graph connections
                graph_smoothness = cluster_avg_capability.T @ self.graph_laplacian @ cluster_avg_capability
                graph_smoothness = max(0, graph_smoothness)  # Ensure non-negative
            else:
                graph_smoothness = 0.0
            
            # Parameter mapping with graph awareness
            base_prior = 0.1 + overall_capability * 0.6
            base_learning = 0.2 + overall_capability * 0.4
            base_slip = 0.3 * (1 - overall_capability)
            base_guess = 0.1 + (1 - overall_capability) * 0.2
            
            # Adjust based on graph smoothness
            # High smoothness = skills are well-connected, boost learning rate
            smoothness_factor = min(graph_smoothness / len(self.skills), 0.1)
            
            bkt_params = {
                'prior_knowledge': min(0.8, base_prior + smoothness_factor * 0.1),
                'learning_rate': min(0.7, base_learning + smoothness_factor * 0.2),
                'slip_rate': max(0.01, base_slip - smoothness_factor * 0.05),
                'guess_rate': base_guess
            }
            
            self.cluster_bkt_parameters[cluster_id] = bkt_params
            
            print(f" Cluster {cluster_id} ({len(cluster_students)} students):")
            print(f"  Average capability: {overall_capability:.3f}")
            print(f"  Graph smoothness: {graph_smoothness:.4f}")
            print(f"  BKT params: P(L₀)={bkt_params['prior_knowledge']:.3f}, "
                  f"P(T)={bkt_params['learning_rate']:.3f}, "
                  f"P(S)={bkt_params['slip_rate']:.3f}, "
                  f"P(G)={bkt_params['guess_rate']:.3f}")
    
    def train_clusters(self, students_data, skills):
        """
        Complete training for Graph Laplacian PCBKT system
        """        
        print("Starting Graph Laplacian PCBKT training...")
        
        # Step 1: Build capability matrix from student data
        capability_matrix = self.build_capability_matrix(students_data, skills)
        
        # Step 2: Apply graph Laplacian regularized dimensionality reduction
        processed_data = self.apply_graph_laplacian_svd(capability_matrix)
        
        # Step 3: Discover clusters
        cluster_labels = self.discover_clusters(processed_data)
        
        # Step 4: Calculate BKT parameters
        self.calculate_cluster_parameters(capability_matrix, cluster_labels)
        
        print("Graph Laplacian PCBKT training complete")
        return cluster_labels
    
    def assign_new_student(self, diagnostic_results):
        """
        Assign New Student to Cluster using graph-aware processing
        """
        if self.kmeans_model is None:
            raise ValueError("Must train clusters first")
        
        if self.graph_aware_components is None:
            raise ValueError("Graph-aware components not available")
                
        # Convert diagnostic to capability vector
        new_capabilities = self.diagnostic_to_capabilities(diagnostic_results)
        
        # Apply same graph-aware transformation as training
        capabilities_centered = new_capabilities - np.mean(new_capabilities)
        processed_capabilities = capabilities_centered @ self.graph_aware_components
        
        # Assign to closest cluster in reduced space
        cluster_id = self.kmeans_model.predict([processed_capabilities])[0]
        
        # Get BKT parameters for this cluster
        bkt_params = self.cluster_bkt_parameters[cluster_id]
        
        # Calculate confidence in assignment
        confidence = self.calculate_assignment_confidence(processed_capabilities, cluster_id)
        
        result = {
            'assigned_cluster': cluster_id,
            'estimated_capabilities': new_capabilities,
            'bkt_parameters': bkt_params,
            'assignment_confidence': confidence,
            'graph_aware_processing': self.use_graph_laplacian,
            'dimensionality_reduction': f"{len(self.skills)} → {self.n_components}"
        }
        
        print(f"Student assigned to cluster {cluster_id}")
        print(f"Confidence: {confidence:.3f}")
        print(f"Used graph structure: {self.use_graph_laplacian}")
        print(f"BKT P(L₀): {bkt_params['prior_knowledge']:.3f}")
        
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
                # Could use graph structure to infer from related skills
                capability = self.infer_capability_from_graph(skill, diagnostic_results)
            
            capabilities.append(capability)
        
        return np.array(capabilities)
    
    def infer_capability_from_graph(self, target_skill, diagnostic_results):
        """
        Infer capability for untested skill using graph connections
        """
        if not self.use_graph_laplacian or self.knowledge_graph is None:
            return 0.3  # Conservative default
        
        # Find connections to tested skills
        target_idx = self.skill_to_index.get(target_skill, -1)
        if target_idx == -1:
            return 0.3
        
        # Get adjacency information for this skill
        adjacency_matrix = self.knowledge_graph.get_adjacency_matrix()
        if adjacency_matrix.size == 0 or target_idx >= adjacency_matrix.shape[0]:
            return 0.3
        
        # Find connected skills that were tested
        weighted_capability = 0.0
        total_weight = 0.0
        
        for skill, result in diagnostic_results.items():
            skill_idx = self.skill_to_index.get(skill, -1)
            if skill_idx != -1 and skill_idx < adjacency_matrix.shape[0]:
                # Check connection strength
                connection_weight = max(
                    adjacency_matrix[target_idx, skill_idx],
                    adjacency_matrix[skill_idx, target_idx]
                )
                
                if connection_weight > 0.1:  # Only use meaningful connections
                    capability = result['correct'] / result['total'] if result['total'] > 0 else 0.3
                    weighted_capability += capability * connection_weight
                    total_weight += connection_weight
        
        if total_weight > 0:
            return weighted_capability / total_weight
        else:
            return 0.3  # No connections found
    
    def calculate_assignment_confidence(self, capabilities, assigned_cluster):
        """
        Calculate confidence in cluster assignment in reduced space
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
    
    def get_cluster_analysis(self):
        """
        Get detailed analysis of discovered clusters
        """
        if not self.cluster_bkt_parameters:
            return {"error": "No clusters trained yet"}
        
        analysis = {
            'n_clusters': self.n_clusters,
            'dimensionality_reduction': f"{len(self.skills)} → {self.n_components}",
            'graph_laplacian_used': self.use_graph_laplacian,
            'laplacian_weight': self.laplacian_weight,
            'clusters': {}
        }
        
        for cluster_id, params in self.cluster_bkt_parameters.items():
            cluster_info = {
                'bkt_parameters': params,
                'avg_capabilities': self.cluster_avg_capabilities.get(cluster_id, []),
                'capability_mean': float(np.mean(self.cluster_avg_capabilities.get(cluster_id, [0]))),
                'capability_std': float(np.std(self.cluster_avg_capabilities.get(cluster_id, [0])))
            }
            analysis['clusters'][cluster_id] = cluster_info
        
        return analysis
    
    # Placeholder methods for counting attempts (to be implemented based on your data structure)
    def count_correct_answers(self, student, skill):
        """Count correct answers for student on given skill"""
        # Implementation depends on your student data structure
        # This is a placeholder
        return getattr(student, 'correct_counts', {}).get(skill, 0)
    
    def count_total_attempts(self, student, skill):
        """Count total attempts for student on given skill"""
        # Implementation depends on your student data structure  
        # This is a placeholder
        return getattr(student, 'total_attempts', {}).get(skill, 0)


# Example usage and testing functions
def test_graph_laplacian_pcbkt(knowledge_graph, student_data, skills):
    """
    Test the Graph Laplacian PCBKT system
    """
    print(" Testing Graph Laplacian PCBKT...")
    
    # Create and configure system
    gl_pcbkt = GraphLaplacianPCBKT(
        n_clusters=3,
        use_graph_laplacian=True,
        laplacian_weight=0.3,
        svd_threshold=0.90
    )
    
    # Set knowledge graph reference
    gl_pcbkt.set_knowledge_graph(knowledge_graph)
    
    # Train the system
    cluster_labels = gl_pcbkt.train_clusters(student_data, skills)
    
    # Get analysis
    analysis = gl_pcbkt.get_cluster_analysis()
    
    return gl_pcbkt, cluster_labels, analysis

def compare_with_without_graph_laplacian(knowledge_graph, student_data, skills):
    """
    Compare clustering with and without graph Laplacian regularization
    """
    print(" Comparing standard vs graph-aware clustering...")
    
    # Standard approach
    standard_pcbkt = GraphLaplacianPCBKT(
        n_clusters=3,
        use_graph_laplacian=False,
        svd_threshold=0.90
    )
    standard_pcbkt.set_knowledge_graph(knowledge_graph)
    standard_labels = standard_pcbkt.train_clusters(student_data, skills)
    
    print("\n" + "="*50)
    
    # Graph Laplacian approach
    graph_pcbkt = GraphLaplacianPCBKT(
        n_clusters=3, 
        use_graph_laplacian=True,
        laplacian_weight=0.3,
        svd_threshold=0.90
    )
    graph_pcbkt.set_knowledge_graph(knowledge_graph)
    graph_labels = graph_pcbkt.train_clusters(student_data, skills)
    
    return {
        'standard': (standard_pcbkt, standard_labels),
        'graph_aware': (graph_pcbkt, graph_labels)
    }