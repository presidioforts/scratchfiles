

import jenkins.model.Jenkins

pipeline {
    agent any
    stages {
        stage('Check Executors with Label') {
            steps {
                script {
                    // Define the specific label you want to check
                    def label = 'your-label' // Replace 'your-label' with your actual label

                    // Filter nodes with the specified label
                    def nodesWithLabel = Jenkins.instance.nodes.findAll { it.assignedLabels*.name.contains(label) }

                    // Calculate total and idle executors for nodes with this label
                    def totalExecutorsWithLabel = nodesWithLabel.sum { it.numExecutors }
                    def idleExecutorsWithLabel = nodesWithLabel.sum { it.countIdle() }

                    echo "Total Executors with label '${label}': ${totalExecutorsWithLabel}"
                    echo "Idle Executors with label '${label}': ${idleExecutorsWithLabel}"
                }
            }
        }
    }
}
