
task appNpmBuild(type: NpmTask) {
    description = "Builds production version of the webapp"
    workingDir = file("${project.projectDir}/src/main/webapp")
    args = ["run", "build", "--", "--verbose"]
    environment "CI", "true"
    environment "NODE_OPTIONS", "--trace-warnings --max_old_space_size=4096"
    environment "INLINE_RUNTIME_CHUNK", "false"
    environment "GENERATE_SOURCEMAP", "false"
}
