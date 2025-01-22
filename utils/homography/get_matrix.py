import numpy as np

def get_Ai(x, xp, homogen=False):
    # convert x_i, xp_i to homogeneous coords
    if not homogen:
        x_i = np.concatenate((x, [1]))
        xp_i = np.concatenate((xp, [1]))
    else:
        x_i = x
        xp_i = xp
    row1 = np.concatenate((
        np.zeros(3),
        -xp_i[-1]*x_i,
        xp_i[1]*x_i
    )
    )
    row2 = np.concatenate((
         xp_i[-1]*x_i,
         np.zeros(3),
         -xp_i[0]*x_i
    ))
    return np.array([row1, row2])

def get_A(x, x_prime, homogen=False):
    A = np.zeros((0,9))
    for i in range(x.shape[0]):
        Ai = get_Ai(x[i], x_prime[i], homogen)
        A = np.concatenate((A,Ai))
    return A
