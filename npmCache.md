# gradle.properties
org.gradle.caching=true
cacheDir=${user.home}/.gradle/caches/${branchName}

// build.gradle
if (project.hasProperty('branchName')) {
    def branchName = project.property('branchName')
    gradle.startParameter.buildCacheDir = new File("${System.getenv('HOME')}/.gradle/caches/${branchName}")
}

