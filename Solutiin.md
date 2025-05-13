
<Project Sdk="Microsoft.NET.Sdk">

  <!-- Grab the env‑var when MSBuild starts -->
  <PropertyGroup>
    <BuildNumber>$([System.Environment]::GetEnvironmentVariable('BUILD_NUMBER'))</BuildNumber>
  </PropertyGroup>

  <!-- Generate one .g.cs file before the compiler runs -->
  <Target Name="GenBuildInfo" BeforeTargets="Compile">
    <WriteLinesToFile
        File="BuildInfo.g.cs"
        Lines='namespace BuildInfo { internal static class Info { public const string BuildNumber = "$(BuildNumber)"; } }'
        Overwrite="true" />
    <Compile Include="BuildInfo.g.cs" />
  </Target>

</Project>
