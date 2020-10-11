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

// Height

Extended_Height = false;

// Top

Top_Style = "logo_sm"; // [base_mm2:Plain - Two Materials, logo_mm2:Logo - Two Materials, logo_mm3:Logo - Three Materials, hex_mm2:Hexagons - Two Materials, pihole_mm4:Pi-hole Logo - Four Materials]

/* [Fan Features] */

Fan_Type = "30mm"; // [30mm, 40mm]
Fan_Hole = false;

/* [Accessory Features] */

Cam_Slot = false;

/**********************************************************/
/* Case Generation                                        */
/**********************************************************/

validation();

rotate(180, [0,1,0] ) {
    
    difference() {
     
        union() {
            
            case_mesh();
            fan_hole_border_mesh();
            
        }
        
        cam_slot_mesh();
        
    }
    
}

/**********************************************************/
/* Modules                                                */
/**********************************************************/

/*--------------------------------------------------------*/
/* Validation                                             */
/*--------------------------------------------------------*/

module validation() {
    
    // This validation aims to rule out combinations that
    // will most likly be problematic to print. Feel free
    // to remove them if you want to give it a try anyway.
    
}

/*--------------------------------------------------------*/
/* Case Style                                             */
/*--------------------------------------------------------*/

// Case

module case_mesh() {
    
    if (Extended_Height) {
        
        if (Top_Style == "logo_mm2") {
            
            import("z_top_h20_style_logo_mm2_c2_base.stl");
            
        } else if (Top_Style == "logo_mm3") {
            
            import("z_top_h20_style_logo_mm3_c2_base.stl");
            
        } else if (Top_Style == "hex_mm2") {
            
            if (Fan_Hole) {
                
                if (Fan_Type == "30mm") {
                    import("z_top_h20_style_hex_mm2_c2_fan30_base.stl");
                } else {
                    import("z_top_h20_style_hex_mm2_c2_fan40_base.stl");
                }
                
            } else {

                import("z_top_h20_style_hex_mm2_c2_base.stl");
                
            }
                
        } else if (Top_Style == "pihole_mm4") {
            
            import("z_top_h20_style_pihole_mm4_c2_base.stl");
            
        }
        
    } else {
    
        if (Top_Style == "logo_mm2") {
            
            import("z_top_style_logo_mm2_c2_base.stl");
            
        } else if (Top_Style == "logo_mm3") {
            
            import("z_top_style_logo_mm3_c2_base.stl");
            
        } else if (Top_Style == "hex_mm2") {
            
            if (Fan_Hole) {
                
                if (Fan_Type == "30mm") {
                    import("z_top_style_hex_mm2_c2_fan30_base.stl");
                } else {
                    import("z_top_style_hex_mm2_c2_fan40_base.stl");
                }
                
            } else {

                import("z_top_style_hex_mm2_c2_base.stl");
                
            }
                
        } else if (Top_Style == "pihole_mm4") {
            
            import("z_top_style_pihole_mm4_c2_base.stl");
            
        }
        
    }
    
}

/*--------------------------------------------------------*/
/* Fan Features                                           */
/*--------------------------------------------------------*/

module fan_hole_border_mesh() {
    
    if (Fan_Hole) {

        if (Extended_Height) {
            
            if (Fan_Type == "30mm") {
                import("z_top_h20_fan30_hole_border_mm2_c2_base.stl");
            } else {
                import("z_top_h20_fan40_hole_border_mm2_c2_base.stl");
            }
            
        } else {
            
            if (Fan_Type == "30mm") {
                import("z_top_fan30_hole_border_mm2_c2_base.stl");
            } else {
                import("z_top_fan40_hole_border_mm2_c2_base.stl");
            }
            
        }

    }
    
}

/*--------------------------------------------------------*/
/* Accessory Features                                     */
/*--------------------------------------------------------*/

module cam_slot_mesh() {
    
    if (Cam_Slot) {
        
        if (Extended_Height) {
            
            if (Top_Style == "hex_mm2") {
                
                if (Fan_Type == "40mm" && Fan_Hole) {
                    import("z_top_h20_cam_slot_style_hex_fan40_cut.stl");
                } else {
                    import("z_top_h20_cam_slot_style_hex_cut.stl");
                }
                
            } else {

                if (Fan_Type == "40mm" && Fan_Hole) {
                    import("z_top_h20_cam_slot_fan40_cut.stl");
                } else {
                    import("z_top_h20_cam_slot_cut.stl");
                }

            }
            
        } else {

            if (Top_Style == "hex_mm2") {

                if (Fan_Type == "40mm" && Fan_Hole) {
                    import("z_top_cam_slot_style_hex_fan40_cut.stl");
                } else {
                    import("z_top_cam_slot_style_hex_cut.stl");
                }

            } else {

                if (Fan_Type == "40mm" && Fan_Hole) {
                    import("z_top_cam_slot_fan40_cut.stl");
                } else {
                    import("z_top_cam_slot_cut.stl");
                }

            }

        }
        
    }
    
}