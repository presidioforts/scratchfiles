<Target Name="Debug‑Secrets" BeforeTargets="Deploy">
  <!-- Only the first 4 characters are printed -->
  <PropertyGroup>
    <SecretPreview>$([System.String]::Copy('$(MY_SECRET)').Substring(0,4))***</SecretPreview>
  </PropertyGroup>

  <Message Text="ApiKey starts with: $(SecretPreview)" Importance="high"/>
</Target>
