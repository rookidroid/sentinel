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

Top_Style = "pihole_mm4"; // [pihole_mm4:Pi-hole Logo - Four Materials]

/* [Accessory Features] */

Cam_Slot = false;

/**********************************************************/
/* Case Generation                                        */
/**********************************************************/

validation();

rotate(180, [0,1,0] ) {
    
    difference() {
        case_mesh();
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
        
        if (Top_Style == "pihole_mm4") {
            import("z_top_h20_style_pihole_mm4_c4_base.stl");
        }
        
    } else {
    
        if (Top_Style == "pihole_mm4") {
            import("z_top_style_pihole_mm4_c4_base.stl");
        }
        
    }
    
}

/*--------------------------------------------------------*/
/* Accessory Features                                     */
/*--------------------------------------------------------*/

module cam_slot_mesh() {
    
    if (Cam_Slot) {
        
        if (Extended_Height) {
            import("z_top_h20_cam_slot_cut.stl");
        } else {
            import("z_top_cam_slot_cut.stl");
        }
        
    }
    
}