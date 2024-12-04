
pitest {
    targetClasses = ['com.wellsfargo.npl.npi.facilient.service.*']
    targetTests = ['com.wellsfargo.npl.npi.facilient.*Test']
    threads = 8
    mutators = ['DEFAULTS']
    excludedClasses = ['com.wellsfargo.npl.npi.facilient.exception.*', 'com.wellsfargo.npl.npi.facilient.util.*']
    excludedMethods = ['toString', 'hashCode', 'equals', 'log*']
    timeoutConstInMillis = 5000
    timeoutFactor = 1.5
    verbose = false
    historyInputLocation = file("$buildDir/pitest-history/input")
    historyOutputLocation = file("$buildDir/pitest-history/output")
    incrementalAnalysis = true
    failWhenNoMutations = false
    jvmArgs = ['-Xmx4G']
    excludedTests = ['com.wellsfargo.npl.npi.facilient.integration.*']
}
