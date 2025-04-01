
^bootstrap-service-[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-deploy\.jar$


Explanation:

^ – Start of filename

bootstrap-service- – Literal match

[0-9]+\.[0-9]+\.[0-9]+ – Semantic versioning like 2025.03.311

-[0-9]+ – Timestamp like 20250328.174801-1

-deploy.jar$ – Ends with -deploy.jar
