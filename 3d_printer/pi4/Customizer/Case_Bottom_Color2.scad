/**********************************************************/
/* Malolo's screw-less / snap fit Raspberry Pi 4 Model B  */
/* Case                                                   */
/**********************************************************/
/*                                                        */
/* Use this script generator to customize your Raspberry  */
/* Pi case according to your needs.                       */
/*                                                        */
/**********************************************************/
/*                                                        */
/* Visit me on Thingiverse: :                             */
/*   -> https://www.thingiverse.com/Malolo                */
/*                                                        */
/**********************************************************/

/**********************************************************/
/* Configuration                                          */
/**********************************************************/

/* [Case Style] */

// Bottom

Bottom_Style = "hex_mm2"; // [hex_mm2:Hexagons - Two Materials]

/**********************************************************/
/* Case Generation                                        */
/**********************************************************/

case_mesh();

/**********************************************************/
/* Modules                                                */
/**********************************************************/

module case_mesh(case_name) {
    
    if (Bottom_Style == "hex_mm2") {
        import("z_bottom_style_hex_mm2_c2_base.stl");
    }
    
}