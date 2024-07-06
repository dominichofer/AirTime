#version 330 core

in vec3 normal;
in vec3 fragPos;

layout (location = 0) out vec4 fragColor;

uniform vec3 color;

void main()
{
    // ambient light
    vec3 ambient = vec3(0.5, 0.5, 0.5);

    // diffuse light
    vec3 n = normalize(normal);
    vec3 lightPos1 = vec3(0, 100, 10);
    vec3 lightPos2 = vec3(30, 100, -100);
    vec3 lightPos3 = vec3(0, -100, 100);
    vec3 light_dir1 = normalize(lightPos1 - fragPos);
    vec3 light_dir2 = normalize(lightPos2 - fragPos);
    vec3 light_dir3 = normalize(lightPos3 - fragPos);
    vec3 diffuse1 = vec3(0.8, 0.8, 0.8) * max(0, dot(light_dir1, n));
    vec3 diffuse2 = vec3(0.6, 0.6, 0.6) * max(0, dot(light_dir2, n));
    vec3 diffuse3 = vec3(0.2, 0.2, 0.2) * max(0, dot(light_dir3, n));
    vec3 diffuse = diffuse1 + diffuse2 + diffuse3;

    fragColor = vec4(color * (ambient + diffuse), 1.0);
}
