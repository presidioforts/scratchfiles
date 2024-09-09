
if (env.BRANCH_NAME == "main" || env.BRANCH_NAME == "develop" || env.BRANCH_NAME.startsWith("release")) {
    // Check if there's a slash in the branch name
    if (env.BRANCH_NAME.contains("/")) {
        env.RELEASE_NUMBER = env.BRANCH_NAME.split("/")[1]
    } else {
        // Fallback if no slash is found
        env.RELEASE_NUMBER = env.BRANCH_NAME
    }
} else {
    // Handling PR builds with "PR-<number>/<build_number>"
    if (env.BRANCH_NAME.startsWith("PR-")) {
        def prParts = env.BRANCH_NAME.split("/")[0].split("PR-") // Extract PR number
        env.PR_NUMBER = prParts[1] // PR number from "PR-14"
        env.BUILD_NUMBER = env.BRANCH_NAME.split("/")[1] // Build number from "/4"
    } else if (env.BRANCH_NAME.contains("/")) {
        env.RELEASE_NUMBER = env.BRANCH_NAME.split("/")[1]
    } else {
        env.RELEASE_NUMBER = env.BRANCH_NAME
    }
    env.SNAPSHOT_BUILD = true
    env.SNAPSHOT_DEPLOY = true
}
