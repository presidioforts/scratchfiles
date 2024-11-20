import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

String branchName = "release/nov5thoffcycle";
String encodedBranchName = URLEncoder.encode(branchName, StandardCharsets.UTF_8.toString());
// encodedBranchName will be "release%2Fnov5thoffcycle"
