Feature Request: Conan Support and Enhanced Build Types for CPP Buildpack

Feature Description:

Conan Support Integration:

Enable Conan package manager support directly within the existing CPP buildpack. This eliminates the need to maintain a separate CMake buildpack, thus streamlining the buildpack ecosystem.


Snapshot and Developer Build Types:

Introduce Snapshot and Developer build types explicitly in the CPP buildpack. This allows artifacts to be appropriately retained or discarded based on build context, significantly optimizing artifact management and reducing storage overhead.



Justification:

1. Simplified Buildpack Management:

Currently, maintaining separate CPP and CMake buildpacks introduces unnecessary complexity and resource overhead. Merging Conan support into the CPP buildpack simplifies buildpack management, enhances maintainability, and reduces development redundancy.



2. Optimized Artifact Retention:

The absence of explicit Snapshot and Developer build types results in inefficient artifact retention, cluttering the Artifactory with unnecessary build artifacts. Clear differentiation between these build types ensures artifacts are only retained when necessary, optimizing storage usage and improving system performance.



3. Improved Debugging and Validation:

Clearly defined Developer build types facilitate easier debugging, testing, and PR validations, enhancing the developer experience and improving productivity.



4. Consistency Across Buildpacks:

Implementing Conan and unified build types in CPP buildpack provides a consistent user experience and build strategy across all applications using the CPP buildpack, significantly improving usability and reducing confusion.




Proposed Implementation Steps:

1. Integrate Conan support into the existing CPP buildpack.


2. Clearly define and implement Snapshot and Developer build types.


3. Document the new build types clearly in EPL release notes and internal documentation.


4. Deprecate and subsequently remove the separate CMake buildpack upon successful integration and validation.



Anticipated Benefits:

Enhanced productivity and reduced maintenance complexity.

Optimized artifact storage management.

Improved clarity and usability for developers.

Consistent, efficient, and streamlined build processes.


This strategic enhancement aligns closely with the customer’s request and improves overall operational efficiency.



Please review and let me know if further refinements are needed.

