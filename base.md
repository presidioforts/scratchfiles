pitest {
    threads = 8
    jvmArgs = ['-Xmx4G']
    targetClasses = ['com.wellsfargo.npl.npi.facilient.service.*']
    excludedClasses = ['com.wellsfargo.npl.npi.facilient.util.*', 'com.wellsfargo.npl.npi.facilient.dto.*']
    mutators = ['DEFAULTS']
    incrementalAnalysis = true
    historyInputLocation = file("$buildDir/pitest-history/input")
    historyOutputLocation = file("$buildDir/pitest-history/output")
}
