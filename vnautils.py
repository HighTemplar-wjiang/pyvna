"""Created by Weiwei Jiang on 20180418

Utility methods for VNA.
"""

import numpy as np


def _s2z(s, z_ports):
    """Convert S-parameters to Z-parameters
    https://en.wikipedia.org/wiki/Impedance_parameters

    Args:
        s (complex matrix): S-parameter matrix to be converted.
        z_ports (float or int matrix): Characteristic impedance of measurement ports.

    Returns:
        complex matrix: converted Z-parameter matrix.

    Example:
        S parameters with 50-Ohm measurement ports:
            s = [[s11, s12], [s21, s22]], z_ports = [50, 50] --> [[z11, z12], [z21, z22]]
    """

    num_ports = len(z_ports)
    diag_z = np.eye(num_ports)
    diag_eye = np.eye(num_ports)
    for idx, z_port in enumerate(z_ports):
        diag_z[idx, idx] = np.sqrt(z_port)

    z = np.matmul(diag_z, diag_eye + s)
    z = np.matmul(z, np.linalg.inv(diag_eye - s))
    z = np.matmul(z, diag_z)
    return z


def _z2s(z, z_ports):
    """Convert Z-parameters to S-parameters.
    https://en.wikipedia.org/wiki/Impedance_parameters

    Args:
        z (complex matrix): Z-parameter matrix to be converted.
        z_ports (float or int matrix): Characteristic impedance of measurement ports.

    Returns:
        complex matrix: converted S-parameter matrix.

    Example:
        Z parameters to 75-Ohm measurement ports:
            z = [[z11, z12], [z21, z22]], z_ports = [75, 75] --> [[s11, s12], [s21, s22]]

    """
    num_ports = len(z_ports)
    diag_y = np.eye(num_ports)
    diag_eye = np.eye(num_ports)
    for idx, z_port in enumerate(z_ports):
        diag_y[idx, idx] = 1. / np.sqrt(z_port)

    s_left = np.matmul(np.matmul(diag_y, z), diag_y) - diag_eye
    s_right = np.matmul(np.matmul(diag_y, z), diag_y) + diag_eye
    s = np.matmul(s_left, np.linalg.inv(s_right))
    return s
