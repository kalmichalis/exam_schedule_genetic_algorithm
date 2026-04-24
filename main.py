import pandas as pd
import random



def load_data(arxeio):

    # διαβάζουμε το Excel αρχείο
    df = pd.read_excel(
        arxeio,
        sheet_name=0,
        engine="xlrd"
    )

    # λεξικό με key ΑΜ φοιτητή value λίστα ΘΕ που έχει δηλώσει
    foitites = {}

    for _, grammi in df.iterrows():

        am = grammi.iloc[0]  # ΑΜ φοιτητή

        the_list = []  # η λίστα με τις ΘΕ για τον συγκεκριμένο φοιτητή

        for c in range(1, 6):

            timi = grammi.iloc[c]  # παίρνουμε την καθε ΘΕ που εχει επιλέξει ο φοιτητης

            if pd.notna(timi) and str(timi).strip():#κραταμε μόνο έγκυρες ΘΕ και πετάμε κενά ή άκυρες τιμές
                the_list.append(str(timi).strip())

        # αν ο φοιτητής έχει τουλάχιστον μία ΘΕ, τον κρατάμε
        if the_list:
            foitites[am] = the_list

    # αποθηκεύουμε ταξινομημένα όλες οι μοναδικές ΘΕ που εμφανίζονται στο Excel
    all_the = sorted({
        th
        for lst in foitites.values()
        for th in lst
    })

    return foitites, all_the

#συναρτηση του κατα ποσο ευχαριστημενοι ειναι οι φοιτητες με το συγεκριμενο προγραμμα εξετασης
"""
Ένας φοιτητής θεωρείται ευχαριστημένος από το εξεταστικό πρόγραμμα εάν δεν έχει δύο εξετάσεις την ίδια ημέρα 
και δεν έχει δύο εξετάσεις σε συνεχόμενες ημέρες 
δηλαδη πχ να δινει σημερα και αυριο άρα η αποσταση των ημερων που θα δινει θα πρεπει να ειναι πανω απο 1
"""
def quality_score(programma, foitites):

    happy = 0  # πληθος ευχαριστημενων φοιτητων

    for lst in foitites.values():

        # αν εχει μια θεματικη ενοτητητα τοτε ειναι ενταξει ο φοιτητής καθώς έχει μόνο μια για το τρεχων έτος
        if len(lst) <= 1:
            happy += 1
            continue

        #
        """Διατρέχει όλες τις ΘΕ που έχει δηλώσει ο συγκεκριμένος φοιτητής (η lst είναι η λίστα των ΘΕ του συγκεκριμενου φοιτητη)
            Βρίσκει σε ποια ημέρα έχει τοποθετηθεί η εξέταση αυτής της ΘΕ (το programma[th] είναι ένα λεξικό της μορφής ΘΕ: ημέρα )
            Παίρνουμε όλες αυτές τις ημέρες και τις ταξινομεί σε αύξουσα σειρά ωστε να μπορω να συκγρινω την αποσταση τους αν ειναι πανω απο 1"""
        days = sorted(
            programma[th]
            for th in lst
        )

        ok = True #αρχικα θεωρουμε οτι ο φοιτητης ειναι ευχαριστημενος

        # ελεγχος συγκρουσεων
        for i in range(len(days) - 1):

            # πεφτει το μαθημα την ιδια ημερα
            if days[i] == days[i + 1]:
                ok = False
                break

            # πεφτει το μαθημα την + ή - 1 ημερα με αλλο μαθημα
            if days[i + 1] - days[i] < 2:
                ok = False
                break

        if ok:
            happy += 1 #αυξανω το πληθος των χαρουμενων φοιτητων

    return happy / len(foitites), happy




#αφελες προγραμματα

def naive_schedule(all_the, mix=False):
    """
    το mix αν είναι True ανακατεύει τη σειρά των ΘΕ στην αρχη το πρωτο ειναι κανονικο και στη συνεχεια ανακατευουμε
    """

    # Δημιουργούμε ένα αντίγραφο της λίστας των ΘΕ για να μην αλλάξουμε την αρχική λίστα
    lista = all_the.copy()

    # Αν το mix είναι True, ανακατεύουμε τυχαία τη σειρά για να δούμε διαφορετικές διατάξεις και πώς επηρεάζουν την ποιότητα του προγράμματος
    if mix:
        random.shuffle(lista)

    """αρχικα δημιουγουμε το πρόγραμμα της εξεταστικης που ειναι ενα λεξικο αρχικα αδειο και με το enumerate(lista) δίνει ζεύγη (θέση, ΘΕ)
    πχ (0, 'ΠΛΗ10'), (1, 'ΠΛΗ11'), (2, 'ΠΛΗ12') ....
    Η θέση + 1 γίνεται η ημέρα εξέτασης (1,2,3,...) άρα η πρώτη ΘΕ εξετάζεται ημέρα 1, η δεύτερη ημέρα 2 και ου τω καθε εξης"""

    programma = {}
    for i, th in enumerate(lista):
        programma[th] = i + 1  # i=0 -> ημέρα 1, i=1 -> ημέρα 2, ...

    return programma #επιστρεφουμε το προγραμμα της εξεταστικης


#
#γενετικος αλγορυθμος για το ερωτημα 2

def genetic_algorithm(foitites, all_the, max_days=10, population_size=50, generations=100):
    """
    Βρίσκουμε ένα  εξεταστικό πρόγραμμα χρησιμοποιώντας γενετικό αλγόριθμο
    ως παραμέτρους της συναρτησης έχουμε
        foitites       : είναι λεξικό της μορφής {ΑΜ: [ΘΕ1, ΘΕ2, ...(ότι θεματική έχει επιλέξει]}
        all_the        : λίστα με όλες τις ΘΕ που έχει το excel
        max_days       : μέγιστος αριθμός ημερών 10 που θελουμε να εχουμε εξετασεις πχ 10
        population_size: μέγεθος πληθυσμού πχ 50 διαφορετικα εξεταστικα προγραμματα εξετασιτκης
        generations    : αριθμός γενεών πχ 100 δηλαδη ποσες φορες θα τρεξει ο γεετικος αλγορυθμος

    ως επιστρεφομενη τιμη θα εχουμε
        best_programma : το καλύτερο πρόγραμμα που βρέθηκε γενικά από τις 100 γενιές της μορφής (λεξικό {ΘΕ: ημέρα})
    """

    print("\n=== ΕΚΚΙΝΗΣΗ ΓΕΝΕΤΙΚΟΥ ΑΛΓΟΡΙΘΜΟΥ ===")
    print(f"Παράμετροι εισόδου: max_days={max_days}, population={population_size}, γενιές={generations}")

    # δημιουργια αρχικου πληθυσμου αναθεση σε κάθε ΘΕ μια τυχαία ημέρα εξέτασης και δημιουργεί έναν πληθυσμό από πιθανά προγράμματα
    population = []
    for _ in range(population_size):
        programma = {}
        for th in all_the:
            programma[th] = random.randint(1, max_days)
        population.append(programma)


    for gen in range(generations):# κανει loop για κάθε γενια

        # Υπολογισμός fitness για κάθε πρόγραμμα εξεταστικής που δημιουργηθηκε
        fitness_values = []
        for programma in population:
            penalty = 0# ειναι η ποινη για κάθε μη προβλεπόμενη ημερα εξέτασης ιδια ημερα ή +-1 ημερα
            for lst in foitites.values():
                days = sorted(programma[th] for th in lst)
                for i in range(len(days) - 1):
                    if days[i] == days[i + 1]:
                        penalty += 10  # ίδια μέρα  έχουμε ποινή
                    elif days[i + 1] - days[i] < 2:
                        penalty += 10  # συνεχόμενες έχουμε ποινή
            """fitenss επειδη εχουμε ενα προβλημα ελαχιστοποιησης θελουμε να το μεγιστιποιησουμε άρα ειναι fitness = 1 / (1 + penalty)"""
            fitness = 1 / (1 + penalty)
            fitness_values.append(fitness)


        # Δημιουργούμε ζεύγη (fitness, programma) και ταξινομούμε με βάση το fitness kai έχουμε το καλύτερο πρώτο ωστε να ξεορυμε το καλυτερο προγραμμα παντα
        paired = list(zip(fitness_values, population))
        paired.sort(reverse=True, key=lambda x: x[0])  # μεγαλύτερο fitness = καλύτερο
        sorted_population = [p for _, p in paired]

        # Κράτα το καλύτερο μισό απο τα εξεταστικά προγράμματα που έχουμε δημιουργησει μεχρι στιγμής
        best_half = sorted_population[:population_size // 2]

        # Δημιουργία νέου πληθυσμού με τα καλυτερα προγραμματα που εχουν τρεξει μεχρι στιγμης
        new_population = best_half.copy()  # νεα γενια με τα καλυτερα

        # Δημιουργούμε νέα παιδιά δηλαδη προγραμματα μέχρι να γεμίσει ο πληθυσμός
        while len(new_population) < population_size:
            # Επιλογή δύο γονέων τυχαια
            p1 = random.choice(best_half)
            p2 = random.choice(best_half)

            # διασταύρωση για κάθε ΘΕ, παίρνουμε τυχαία από τον έναν ή τον άλλο γονέα με random με πιθανοτητα 0-0,5 απο τον 1ο γονεα και 0,5-1 απο τον αλλο
            child = {}
            for th in all_the:
                if random.random() <= 0.5:
                    child[th] = p1[th]
                else:
                    child[th] = p2[th]


            """
             # Μετάλαξη με 20% πιθανότητα απο από random αριθμους 
            όπου τυχαία σε μια ΘΕ την ημέρα με τυχαίο τρόπο με μία άλλη ημερα πχ αν έχουμε την ΠΛΗ31 και άν έχουμε ημέρες εξέτασης 10 τότε από τους αριθμούς 
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10 τότε η ΠΛΗ31 από την ημέρα 3μετά τη μετάλλαξη θα είναι ΠΛΗ31 την 7η ημέρα ή οποιαδήποτε άλλη τυχαία  ημέρα"""
            if random.random() <= 0.2:
                random_th = random.choice(all_the)
                child[random_th] = random.randint(1, max_days)

            new_population.append(child)

        # Αντικατάσταση πληθυσμού
        population = new_population

        # στατιστική εκτύπωση προοδου και debugging  κάθε 5 γενιές
        if gen % 5 == 0:
            best_prog = sorted_population[0]  # το πρώτο είναι το καλύτερο της καθε γενιάς μετά την ταξινόμηση
            score, happy = quality_score(best_prog, foitites)
            print(f"Γενιά {gen:3d}: {score:.2%} ευχαριστημένοι φοιτητές {happy}/{len(foitites)} ευχαριστημένοι)")


    best_programma = sorted_population[0]

    return best_programma



#main

def main():
    arxeio = "imeres_exam.xls"



    foitites, all_the = load_data(arxeio)

    print(f"ΠΛΗΘΟΣ ΦΟΙΤΗΤΩΝ\t\t\t\t\t: {len(foitites)}")
    print(f"ΠΛΗΘΟΣ ΘΕΜΑΤΙΚΩΝ ΕΝΟΤΗΤΩΝ\t\t: {len(all_the)}")


    print("\nΚάθε ΘΕ σε ξεχωριστή ημέρα (5 διαφορετικές διατάξεις)")
    for i in range(5):
        sched = naive_schedule(all_the, mix=(i > 0))
        score, happy = quality_score(sched, foitites)
        print(f"  {i + 1}η διάταξη: {score:.2%} ({happy}/{len(foitites)} ευχαριστημένοι)")



    print("\n\nΕΡΩΤΗΜΑ Β: ΓΕΝΕΤΙΚΟΣ ΑΛΓΟΡΙΘΜΟΣ")


    best = genetic_algorithm(foitites, all_the)

    score, happy = quality_score(best, foitites)

    print("\n")
    print("ΤΕΛΙΚO ΑΠΟΤΕΛΕΣΜΑ")
    print("\n")
    print(f"Ποιότητα εξεταστικού προγράμματος: {score:.2%}")
    print(f"Ευχαριστημένοι φοιτητές: {happy}/{len(foitites)}")
    print(f"Συνολικές ημέρες εξεταστικής: {max(best.values())}")
    print_schedule_by_day(best)

def print_schedule_by_day(programma):

    # αρχικα κανουμε reverse ωστε να ειναι τηνς μορφης ημερα:[λιστα ΘΕ]
    days_dict = {}

    for th, day in programma.items():

        if day not in days_dict:#αν δεν υπαρχει η ημερα προσθεσαι μια αδεια λιστα και μετα προσθετει τις ΘΕ
            days_dict[day] = []

        days_dict[day].append(th)

    print("\nΗ ΚΑΛΥΤΕΡΗ ΔΙΑΤΑΞΗ ΘΕ ΑΝΑ ΗΜΕΡΑ ΠΟΥ ΕΧΟΥΜΕ ΕΙΝΑΙ:")

    for day in sorted(days_dict):

        print(f"Ημέρα {day}: {sorted(days_dict[day])}")
        """εδώ οι ημέρες εξετάσεων ταξινομούνται σε αύξουσα σειρά και για κάθε ημέρα και εμφανίζονται 
        οι αντίστοιχες θεματικές ενότητες σε ταξινομημένη σειρά, ώστε η τελική διάταξη να παρουσιάζεται με σωστό τρόπο"""


if __name__ == "__main__":
    main()