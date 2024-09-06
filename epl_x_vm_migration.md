
# EPL-X CI/CD Workflow Automation Product

EPL-X is a new CI/CD workflow automation product built using GitHub Action-based technology. It’s a SaaS product that offers a basic build pack and modern development toolkits to create new automation workflows. The product uses ephemeral runners, which are created when a job starts and destroyed once the job is done. For VM migration automation, we need a secure environment with no cached data, and that’s why we chose this product to build our VM migration automation.

## VM Migration Buildpack Delivery

We are delivering the VM migration buildpack to LOB organizations so developers can use it as a self-service tool to migrate VMs. Through ELMA onboarding, users can select the new VM migration buildpack and submit their order. ELMA will then create the VM migration repository and copy all the workflow YAML files. Developers can start using it right away.

As part of the product, we provide common use case workflow files, but LOBs can easily add more workflows if needed.
