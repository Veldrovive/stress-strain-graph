from matplotlib import pyplot as plt
import numpy as np

loads = [0, 7.3, 15.1, 23.1, 30.4, 34.4, 38.4, 41.3, 44.8, 46.2, 47.3, 47.5, 46.1, 44.8, 42.6, 36.4]
lengths = [50.8, 50.851, 50.902, 50.952, 51.003, 51.054, 51.308, 51.816, 52.832, 53.848, 54.864, 55.88, 56.896, 57.658, 58.42, 59.182]

l_0 = 50.8
d_0 = 12.8
E = 60


def compute_stresses(loads, diameter):
    s = []
    A = np.pi*(diameter/2)**2
    for force in loads:
        s.append(force/A)
    return s


def compute_strains(lengths, length):
    s = []
    for n_length in lengths:
        s.append((n_length-length)/length)
    return s


def interpolate_stresses(stress):
    # Find the strain that is expected at this stress by linearly interpolating between known stress strain points
    all_above = [i for i, s in enumerate(stresses) if s > stress]
    all_below = [i for i, s in enumerate(stresses) if s <= stress and i < all_above[0]]
    index_above, index_below = all_above[0], all_below[-1]
    stress_above, stress_below = stresses[index_above], stresses[index_below]
    strain_above, strain_below = strains[index_above], strains[index_below]
    next_stress_diff, cur_stress_dif = stress_above-stress_below, stress-stress_below
    next_strain_diff = strain_above-strain_below
    return (cur_stress_dif/next_stress_diff)*next_strain_diff + strain_below


stresses = compute_stresses(loads, d_0)
strains = compute_strains(lengths, l_0)


def graph_stress_strain(stress, strain):
    xs = np.array(strain)
    linear = xs*60
    linear_diff = linear-np.array(stress)
    nonlinear_index = [i for i, d in enumerate(linear_diff) if d > 0.01][0]
    nonlinear_stress = stress[nonlinear_index]
    ultimate_stress = max(stress)
    fracture_stress = stress[-1]
    plt.clf()
    plt.rcParams["figure.figsize"] = (15, 9)


    plt.plot(xs, linear, color='y')
    plt.axhline(y=nonlinear_stress, label="Yield Stress", color='r')
    plt.axhline(y=ultimate_stress, label="Ultimate Stress", color='m')
    plt.axhline(y=fracture_stress, label="Fracture Stress", color='g')
    plt.plot(strain, stress)


    plt.xlabel("Strain")
    plt.ylim(0, max(stress)*1.2)
    plt.ylabel("Stress (GPa)")
    plt.title("Stress Strain Curve")
    plt.legend()
    plt.savefig("stress_strain.png")
    return nonlinear_stress, ultimate_stress, fracture_stress

yield_stress, ultimate_stress, fracture_stress = graph_stress_strain(stresses, strains)
print(f"Yield Stress: {round(1000*yield_stress, 2)}MPa. Ultimate Stress: {round(1000*ultimate_stress, 2)}MPa. Fracture Stress: {round(1000*fracture_stress, 2)}MPa")


def graph_plastic_elastic_strain(stress, strain, release_stress):
    release_strain = interpolate_stresses(release_stress)
    xs = np.linspace(0, release_strain, 10)
    linear = ((xs-release_strain) * 60) + release_stress
    final_strain = release_strain - release_stress / 60
    print("Release Strain:", release_strain)
    plt.clf()
    plt.rcParams["figure.figsize"] = (15, 9)
    plt.plot(strain, stress)
    plt.plot(xs, linear)
    # plt.axhline(y=release_stress)
    # plt.axvline(x=release_strain)
    # plt.axvline(x=final_strain)
    plt.xlabel("Strain")
    plt.ylim(0, max(stress) * 1.2)
    plt.ylabel("Stress (GPa)")
    plt.title("Stress Strain Curve with plastic strain")
    plt.savefig("stress_strain_elastic_plastic.png")
    return final_strain, release_strain

fs, rs = graph_plastic_elastic_strain(stresses, strains, 0.3)
print(f"Plastic strain: {fs}. Elastic Strain: {rs-fs}")

if __name__ == "__main__":
    print("Ran")