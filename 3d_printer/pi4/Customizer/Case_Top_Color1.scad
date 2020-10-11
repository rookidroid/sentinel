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

Top_Style = "logo_sm"; // [base_sm:Plain - Single Material, base_mm2:Plain - Two Materials, logo_sm:Logo - Single Material, logo_mm2:Logo - Two Materials, logo_mm3:Logo - Three Materials, hex_sm:Hexagons - Single Material, hex_mm2:Hexagons - Two Materials, slots_sm:Slots - Single Material, mesh_sm:Mesh - Single Material, pihole_sm:Pi-hole Logo - Single Material, pihole_mm4:Pi-hole Logo - Four Materials]

// Front

Front_Style = "slots"; // [none>:None, slots:Slots, mesh:Mesh]

// Left

Left_Style = "rear_slots"; // [none>:None, rear_slots:Rear Slots, slots:Slots, mesh:Mesh]

// Right

Right_Style = "rear_slots"; // [none>:None, rear_slots:Rear Slots, slots:Slots, mesh:Mesh]

/* [Fan Features] */

Fan_Type = "30mm"; // [30mm, 40mm]
Fan_Hole = false;
Fan_Mounting = "None"; // [none:None, screws:Screws, rails:Rails]

/* [Accessory Features] */

Cam_Slot = false;
Disp_Slot = false;
Pin_Slot = false;

/**********************************************************/
/* Case Generation                                        */
/**********************************************************/

validation();

rotate(180, [0,1,0] ) {
    
    difference() {
     
        union() {
            
            case_mesh();
            
            fan_hole_border_mesh();
            fan_screws_border_mesh();
            fan_rails_mesh();
            
            cam_slot_border_mesh();
            disp_slot_border_mesh();
            pin_slot_border_mesh();
            
        }
        
        front_mesh();
        left_mesh();
        right_mesh();
        
        fan_hole_mesh();
        fan_screws_mesh();
        
        cam_slot_mesh();
        disp_slot_mesh();
        pin_slot_mesh();
        
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
    
    assert(!Fan_Hole || Top_Style != "logo_sm", "Fan Hole can not be used with Logo style");
    
    assert(!Fan_Hole || Top_Style != "logo_mm2", "Fan Hole can not be used with Logo style");    
    
    assert(!Fan_Hole || Top_Style != "logo_mm3", "Fan Hole can not be used with Logo style");

    assert(!Fan_Mounting != "rails" || Top_Style != "mesh_sm", "Fan Rails can not be used with Mesh style");
    
    assert(!Fan_Mounting != "rails" || Fan_Type != "40mm", "Pin Slot can not be used with 40mm Fan Rails");
    
}

/*--------------------------------------------------------*/
/* Case Style                                             */
/*--------------------------------------------------------*/

// Case

module case_mesh() {
    
    if (Extended_Height) {
        
        difference() {
            
            import("z_top_h20_base_sm.stl");
            
            if (Top_Style == "logo_sm") {
                
                import("z_top_h20_style_logo_sm_cut.stl");
                
            } else if (Top_Style == "logo_mm2") {
                
                import("z_top_h20_style_logo_mm2_c1_cut.stl");
                
            } else if (Top_Style == "logo_mm3") {
                
                import("z_top_h20_style_logo_mm3_c1_cut.stl");
                
            } else if (Top_Style == "hex_sm") {
                
                if (Fan_Hole) {
                    
                    if (Fan_Type == "30mm") {
                        import("z_top_h20_style_hex_sm_fan30_cut.stl");
                    } else {
                        import("z_top_h20_style_hex_sm_fan40_cut.stl");
                    }
                    
                } else {
                    
                    import("z_top_h20_style_hex_sm_cut.stl");
                    
                }
                
            } else if (Top_Style == "hex_mm2") {
                
                if (Fan_Hole) {
                    
                    if (Fan_Type == "30mm") {
                        import("z_top_h20_style_hex_mm2_c1_fan30_cut.stl");
                    } else {
                        import("z_top_h20_style_hex_mm2_c1_fan40_cut.stl");
                        
                    }
                    
                } else {

                    import("z_top_h20_style_hex_mm2_c1_cut.stl");
                    
                }
                
            } else if (Top_Style == "slots_sm") {
                
                if (Fan_Hole) {
                    
                    if (Fan_Type == "30mm") {

                        if (Pin_Slot) {
                            import("z_top_h20_style_slots_sm_fan30_pin_slot_cut.stl");
                        } else {
                            import("z_top_h20_style_slots_sm_fan30_cut.stl");
                        }
                            
                    } else {

                        if (Pin_Slot) {
                            import("z_top_h20_style_slots_sm_fan40_pin_slot_cut.stl");
                        } else {
                            import("z_top_h20_style_slots_sm_fan40_cut.stl");
                        }
                        
                    }
                    
                } else {
                    
                    if (Pin_Slot) {
                        import("z_top_h20_style_slots_sm_pin_slot_cut.stl");
                    } else {
                        import("z_top_h20_style_slots_sm_cut.stl");
                    }
                    
                }
                
            } else if (Top_Style == "mesh_sm") {
                
                import("z_top_h20_style_mesh_sm_cut.stl");
                
            } else if (Top_Style == "pihole_sm") {
                
                import("z_top_h20_style_pihole_sm_cut.stl");
                
            } else if (Top_Style == "pihole_mm4") {
                
                import("z_top_h20_style_pihole_mm4_c1_cut.stl");
                
            }
            
        }
        
    } else {
    
        difference() {
            
            import("z_top_base_sm.stl");
            
            if (Top_Style == "logo_sm") {
                
                import("z_top_style_logo_sm_cut.stl");
                
            } else if (Top_Style == "logo_mm2") {
                
                import("z_top_style_logo_mm2_c1_cut.stl");
                
            } else if (Top_Style == "logo_mm3") {
                
                import("z_top_style_logo_mm3_c1_cut.stl");
                
            } else if (Top_Style == "hex_sm") {
                
                if (Fan_Hole) {
                    
                    if (Fan_Type == "30mm") {
                        import("z_top_style_hex_sm_fan30_cut.stl");
                    } else {
                        import("z_top_style_hex_sm_fan40_cut.stl");
                    }
                    
                } else {
                    
                    import("z_top_style_hex_sm_cut.stl");
                    
                }
                
            } else if (Top_Style == "hex_mm2") {
                
                if (Fan_Hole) {
                    
                    if (Fan_Type == "30mm") {
                        import("z_top_style_hex_mm2_c1_fan30_cut.stl");
                    } else {
                        import("z_top_style_hex_mm2_c1_fan40_cut.stl");
                    }
                    
                } else {
                    
                    import("z_top_style_hex_mm2_c1_cut.stl");
                    
                }
                
            } else if (Top_Style == "slots_sm") {
                
                if (Fan_Hole) {
                    
                    if (Fan_Type == "30mm") {
                        
                        if (Pin_Slot) {
                            import("z_top_style_slots_sm_fan30_pin_slot_cut.stl");
                        } else {
                            import("z_top_style_slots_sm_fan30_cut.stl");
                        }
                        
                    } else {

                        if (Pin_Slot) {
                            import("z_top_style_slots_sm_fan40_pin_slot_cut.stl");
                        } else {
                            import("z_top_style_slots_sm_fan40_cut.stl");
                        }
                        
                    }
                    
                } else {
                    
                    if (Pin_Slot) {
                        import("z_top_style_slots_sm_pin_slot_cut.stl");
                    } else {
                        import("z_top_style_slots_sm_cut.stl");
                    }
                    
                }
                
            } else if (Top_Style == "mesh_sm") {
                
                import("z_top_style_mesh_sm_cut.stl");
                
            } else if (Top_Style == "pihole_sm") {
                
                import("z_top_style_pihole_sm_cut.stl");
                
            } else if (Top_Style == "pihole_mm4") {
                
                import("z_top_style_pihole_mm4_c1_cut.stl");
                
            }
            
        }
        
    }
    
}

// Front

module front_mesh() {
    
    if (Front_Style == "slots") {
        
        if (Extended_Height) {
            import("z_top_h20_front_slots_cut.stl");
        } else {
            import("z_top_front_slots_cut.stl");
        }
        
    } else if (Front_Style == "mesh") {
    
        if (Extended_Height) {
            import("z_top_h20_front_mesh_cut.stl");
        } else {
            import("z_top_front_mesh_cut.stl");
        }
    
    }
    
}

// Left

module left_mesh() {
    
    if (Left_Style == "rear_slots") {
    
        if (Extended_Height) {
            import("z_top_h20_left_rear_slots_cut.stl");
        } else {
            import("z_top_left_rear_slots_cut.stl");
        }
        
    } else if (Left_Style == "slots") {
    
        if (Extended_Height) {
            import("z_top_h20_left_slots_cut.stl");
        } else {
            import("z_top_left_slots_cut.stl");
        }
    
    } else if (Left_Style == "mesh") {
    
        if (Extended_Height) {
            import("z_top_h20_left_mesh_cut.stl");
        } else {
            import("z_top_left_mesh_cut.stl");
        }
    
    }
    
}

// Right

module right_mesh() {
    
    if (Right_Style == "rear_slots") {
    
        if (Extended_Height) {
            import("z_top_h20_right_rear_slots_cut.stl");
        } else {
            import("z_top_right_rear_slots_cut.stl");
        }
        
    } else if (Right_Style == "slots") {
    
        if (Extended_Height) {
            import("z_top_h20_right_slots_cut.stl");
        } else {
            import("z_top_right_slots_cut.stl");
        }
    
    } else if (Right_Style == "mesh") {
    
        if (Extended_Height) {
            import("z_top_h20_right_mesh_cut.stl");
        } else {
            import("z_top_right_mesh_cut.stl");
        }
    
    }
    
}

/*--------------------------------------------------------*/
/* Fan Features                                           */
/*--------------------------------------------------------*/

module fan_hole_mesh() {
    
    if (Fan_Hole) {

        if (Extended_Height) {
            
            if (Fan_Type == "30mm") {
                
                if (Top_Style == "base_mm2" || Top_Style ==  "hex_mm2") {
                    import("z_top_h20_fan30_hole_border_mm2_c1_cut.stl");
                } else {
                    import("z_top_h20_fan30_hole_cut.stl");
                }
                
            } else {

                if (Top_Style == "base_mm2" || Top_Style ==  "hex_mm2") {
                    import("z_top_h20_fan40_hole_border_mm2_c1_cut.stl");
                } else {
                    import("z_top_h20_fan40_hole_cut.stl");
                }
            }
            
        } else {
            
            if (Fan_Type == "30mm") {
                
                if (Top_Style == "base_mm2" || Top_Style ==  "hex_mm2") {
                    import("z_top_fan30_hole_border_mm2_c1_cut.stl");
                } else {
                    import("z_top_fan30_hole_cut.stl");
                }
                
            } else {
                
                if (Top_Style == "base_mm2" || Top_Style ==  "hex_mm2") {
                    import("z_top_fan40_hole_border_mm2_c1_cut.stl");
                } else {
                    import("z_top_fan40_hole_cut.stl");
                }
            }
            
        }

    }
    
}

module fan_hole_border_mesh() {
    
    if (Fan_Hole) {
        
        if (Extended_Height) {
            
            if (Fan_Type == "30mm") {
              import("z_top_h20_fan30_hole_border_sm.stl");
            } else {
                import("z_top_h20_fan40_hole_border_sm.stl");
            }
            
        } else {
            
            if (Fan_Type == "30mm") {
                import("z_top_fan30_hole_border_sm.stl");
            } else {
                import("z_top_fan40_hole_border_sm.stl");
            }
            
        }
        
    }
    
}

module fan_screws_mesh() {
    
    if (Fan_Mounting == "screws") {
        
        if (Extended_Height) {
            
            if (Fan_Type == "30mm") {
                import("z_top_h20_fan30_screws_cut.stl");
            } else {
                import("z_top_h20_fan40_screws_cut.stl");
            }
            
        } else {
            
            if (Fan_Type == "30mm") {
                import("z_top_fan30_screws_cut.stl");
            } else {
                import("z_top_fan40_screws_cut.stl");
            }
            
        }
        
    }
    
}

module fan_screws_border_mesh() {

    if (Fan_Mounting == "screws") {

        if (Extended_Height) {

            if (Fan_Type == "30mm") {
                import("z_top_h20_fan30_screws_border.stl");
            } else {
                import("z_top_h20_fan40_screws_border.stl");
            }

        } else {

            if (Fan_Type == "30mm") {
                import("z_top_fan30_screws_border.stl");
            } else {
                import("z_top_fan40_screws_border.stl");
            }

        }

    }

}

module fan_rails_mesh() {
    
    if (Fan_Mounting == "rails") {
        
        if (Extended_Height) {
            
            if (Fan_Type == "30mm") {
                import("z_top_h20_fan30_rails.stl");
            } else {
                import("z_top_h20_fan40_rails.stl");
            }
            
        } else {
            
            if (Fan_Type == "30mm") {
                import("z_top_fan30_rails.stl");
            } else {
                import("z_top_fan40_rails.stl");
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
            
            if (Top_Style == "hex_sm" || Top_Style == "hex_mm2") {
                
                if (Fan_Type == "40mm" && (Fan_Hole || Fan_Mounting != "none")) {
                    import("z_top_h20_cam_slot_style_hex_fan40_cut.stl");
                } else {
                    import("z_top_h20_cam_slot_style_hex_cut.stl");
                }
                
            } else if (Top_Style == "slots_sm") {

                if (Fan_Type == "40mm" && (Fan_Hole || Fan_Mounting != "none")) {
                    import("z_top_h20_cam_slot_style_slots_fan40_cut.stl");
                } else {
                    import("z_top_h20_cam_slot_style_slots_cut.stl");
                }

            } else {

                if (Fan_Type == "40mm" && (Fan_Hole || Fan_Mounting != "none")) {
                    import("z_top_h20_cam_slot_fan40_cut.stl");
                } else {
                    import("z_top_h20_cam_slot_cut.stl");
                }

            }
            
        } else {

            if (Top_Style == "hex_sm" || Top_Style == "hex_mm2") {

                if (Fan_Type == "40mm" && (Fan_Hole || Fan_Mounting != "none")) {
                    import("z_top_cam_slot_style_hex_fan40_cut.stl");
                } else {
                    import("z_top_cam_slot_style_hex_cut.stl");
                }

            } else if (Top_Style == "slots_sm") {

                if (Fan_Type == "40mm" && (Fan_Hole || Fan_Mounting != "none")) {
                    import("z_top_cam_slot_style_slots_fan40_cut.stl");
                } else {
                    import("z_top_cam_slot_style_slots_cut.stl");
                }

            } else {

                if (Fan_Type == "40mm" && (Fan_Hole || Fan_Mounting != "none")) {
                    import("z_top_cam_slot_fan40_cut.stl");
                } else {
                    import("z_top_cam_slot_cut.stl");
                }

            }

        }
        
    }
    
}

module cam_slot_border_mesh(show) {

    if (Cam_Slot) {
        
        if (Extended_Height) {
            
            if (Top_Style == "mesh_sm") {
                
                if (Fan_Type == "40mm" && (Fan_Hole || Fan_Mounting != "none")) {
                    import("z_top_h20_cam_slot_fan40_border.stl");
                } else {
                    import("z_top_h20_cam_slot_border.stl");
                }
                
            }
            
        } else {

            if (Top_Style == "mesh_sm") {

                if (Fan_Type == "40mm" && (Fan_Hole || Fan_Mounting != "none")) {
                    import("z_top_cam_slot_fan40_border.stl");
                } else {
                    import("z_top_cam_slot_border.stl");
                }

            }

        }
        
    }

}

module disp_slot_mesh() {
    
    if (Disp_Slot) {
        
        if (Extended_Height) {
            import("z_top_h20_disp_slot_cut.stl");
        } else {
            import("z_top_disp_slot_cut.stl");
        }
        
    }
    
}

module disp_slot_border_mesh() {
    
    if (Disp_Slot) {
        
        if (Extended_Height) {
            
            if (Top_Style == "mesh_sm") {
                import("z_top_h20_disp_slot_border.stl");
            }
            
        } else {

            if (Top_Style == "mesh_sm") {
                import("z_top_disp_slot_border.stl");
            }
            
        }
        
    }
    
}

module pin_slot_mesh() {
    
    if (Pin_Slot) {
        
        if (Extended_Height) {
            import("z_top_h20_pin_slot_cut.stl");
        } else {
            import("z_top_pin_slot_cut.stl");
        }
        
    }
    
}

module pin_slot_border_mesh() {
    
    if (Pin_Slot) {
        
        if (Extended_Height) {
            
            if (Top_Style == "mesh_sm") {
                import("z_top_h20_pin_slot_border.stl");
            }
            
        } else {
            
            if (Top_Style == "mesh_sm") {
                import("z_top_pin_slot_border.stl");
            }
        }
        
    }
    
}