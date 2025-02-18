If you want to provide feedback without directly giving the fix, you can structure your comments as follows:


---

Subject: Issue in FilterConfig – Missing Request Handling after Forward Removal

Hi [Developer's Name],

I was reviewing the recent changes in FilterConfig, and I noticed a potential issue after the removal of .forward(...). Here are my observations:

1. Requests with a trailing slash (/) are adjusted but not properly handled.

Previously, the request was forwarded after trimming the slash, ensuring it reached the correct handler.

Now, the slash is removed, but nothing is done with the modified requestURI.



2. ALLOWED_PATHS check exists, but there's no defined request flow.

The check if (ALLOWED_PATHS.contains(requestURI)) remains, but without forward(...) or chain.doFilter(...), allowed requests are not processed.

This could result in unexpected behavior where valid API requests don’t get processed correctly.



3. Invalid paths are still blocked, but valid ones may not proceed.

The error response for invalid paths remains (SC_BAD_REQUEST), which is fine.

However, requests that match ALLOWED_PATHS might not be passed along to the next processing step.




Suggested Discussion Points:

What is the intended behavior after removing .forward(...)?

Should requests that pass ALLOWED_PATHS continue in the filter chain instead?

Do we need a check to allow /api/* requests instead of only /api?


Let me know your thoughts. I can help refine the approach based on the expected functionality.

Best,
[Your Name]


---

@Configuration
public class FilterConfig {
    
    private static final Set<String> ALLOWED_PATHS = new HashSet<>();

    static {
        ALLOWED_PATHS.add("/api");  // Allowing only paths under "/api"
    }

    @Bean
    TomcatConnectorCustomizer connectorCustomizer() {
        return connector -> connector.setEncodedSolidusHandling(EncodedSolidusHandling.DECODE.getValue());
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        String requestURI = httpRequest.getRequestURI();

        // Remove trailing slash if present
        if (StringUtils.endsWith(requestURI, "/")) {
            requestURI = StringUtils.removeEnd(requestURI, "/");
        }

        // Check if the request is allowed
        if (ALLOWED_PATHS.stream().anyMatch(requestURI::startsWith)) {
            // Continue processing the request instead of forwarding
            chain.doFilter(request, response);
        } else {
            // Reject invalid requests
            httpResponse.sendError(HttpServletResponse.SC_BAD_REQUEST, "Invalid redirect path");
        }
    }
}

This approach:
✔ Highlights the problem clearly.
✔ Encourages the developer to think about a solution.
✔ Opens up discussion instead of imposing a direct fix.

Would this work for your style of feedback?


