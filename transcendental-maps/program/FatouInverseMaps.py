


import cmath

import cauliflower



def compute_band_distance_to_0 (nb_bands, band_width_inverse, z):
    try:
        log_abs_z = math . log (abs (z))
    except (ValueError):
        return (nb_bands - 1)
    return (round (band_width_inverse * log_abs_z) % nb_bands)



class SimpleFatouInverseMap:

    def __init__ (self, config):

        #self . c = 0.24
        self . large_real_part = config ["large real part"]
                
        return


    def shift_real_part_to_at_least (self, r, z):
        #n = max (0, round (r - z . real) + 1)
        #return z + n, n
        n = max (0, round (z . real + r) + 1)
        return z - n, int (n)

    def shift_to_domain_on_the_far_right (self, z):
        return self . shift_real_part_to_at_least (self . large_real_part, z)


    def compute_preimage_by_F_with_positive_real_part (self, z):
        z_minus_1 = z - 1
        sqrt_discriminant = cmath . sqrt (1 - 4 / (z_minus_1 * z_minus_1))
        if (sqrt_discriminant . real < 0):
            sqrt_discriminant = - sqrt_discriminant
        preimage = 0.5 * z_minus_1 * (1 + sqrt_discriminant)
        return preimage

    def eval_inverse_fatou_coordinates (self, z):
        z_shifted, n_shift = self . shift_to_domain_on_the_far_right (z)
        try:
            phi_z = z_shifted #- math . log (n_shift)
        except (ValueError):
            print ("n_shift=" + str (n_shift))
            print ("z=" + str (z))
            print ("R=" + str (self . large_real_part))
            raise
        #for k in range (n_shift):
        #    phi_z = compute_preimage_by_F_with_positive_real_part (phi_z)
        for k in range (n_shift):
            phi_z = cauliflower . eval_F (phi_z)

        #print ("phi_z = " + str (phi_z))
            
        return -1 / phi_z


    def eval_repelling_fatou_coordinates (self, z):
        raise Exception ("Does not work")
        Z = - 1 / z
        n_shift = 0
        while (Z . real < self . large_real_part):
            Z = cauliflower . eval_F (Z)
            n_shift += 1
            if (n_shift > self . too_much_iterations):
                raise Exception ("Too much iterations")
        return Z - n_shift

    def eval_rescaled_inverse_fatou_coordinates (self, rescaling_factor, z):
        #print ("resc_f = " + str (rescaling_factor))
        return (rescaling_factor * self . eval_inverse_fatou_coordinates  (z))

