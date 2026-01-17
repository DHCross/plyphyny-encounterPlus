void main() {
    float speed = u_time * u_speed * 0.05;
    float strength = u_strength / 100.0;

    vec2 coord = v_tex_coord;

    coord.x += sin((coord.x + speed) * u_frequency) * strength;
    coord.y += cos((coord.y + speed) * u_frequency) * strength;

    gl_FragColor = texture2D(u_texture, coord) * v_color_mix.a;
}
//void main() {
//    vec4 color = SKDefaultShading();
//    gl_FragColor = vec4(0.0, color.g * color.a, 0.0, color.a);
//}
//
//void main() {
//    // get the color of the current pixel
//    vec4 current_color = texture2D(u_texture, v_tex_coord);
//
//    // the center of our circle
//    vec2 circle_center = vec2(0.5, 0.5);
//    vec4 u_first_color = vec4(0);
//    vec4 u_second_color = vec4(1);
//
//    // how far our pixel is from the center of the circle, doubled and clamped so the range is 0.0 to 1.0
//    float pixel_distance = min(1.0, distance(v_tex_coord, circle_center) * 2.0);
//
//    // if the current color is not transparent
//    if (current_color.a > 0.0) {
//        // mix the first color with the second color by however far away we are,
//        // multiplying by this pixel's alpha (to avoid a hard edge) and also
//        // multiplying by the node alpha so we can fade in or out
//        vec4 new_color = mix(u_first_color, u_second_color, pixel_distance);
//        gl_FragColor = vec4(mix(current_color, new_color, new_color.a)) * current_color.a * v_color_mix.a;
//    } else {
//        // use the current (transparent) color
//        gl_FragColor = current_color;
//    }
//}
