import itertools
import random
import time

class BigTwo:
    #inisiasi
    def __init__(self):
        self.suits = ['Diamond', 'Club', 'Heart', 'Spade']
        self.values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        self.deck = self.buat_deck() #mendapat deck
        self.pemain = [[] for _ in range(4)] #asumsi 4 pemain
        self.bagikan_kartu() #membagi kartu
        self.tumpukan_terakhir = [] #belum mulai
        self.giliran = 0 

    def buat_deck(self):
        return [(nilai, jenis) for nilai in self.values for jenis in self.suits]

    def bagikan_kartu(self):
        deck_diacak = self.deck.copy()
        random.shuffle(deck_diacak)
        for i, kartu in enumerate(deck_diacak):
            self.pemain[i % 4].append(kartu)
        for pemain in self.pemain:
            pemain.sort(key=lambda x: (self.values.index(x[0]), self.suits.index(x[1])))

    def bisa_dilakukan(self, kartu, tumpukan): 
        if not tumpukan: 
            return True
        if len(kartu) != len(tumpukan): #jika tidak ada yang lebih besar
            return False
        return self.values.index(kartu[0][0]) > self.values.index(tumpukan[0][0])

    def semua_kombinasi(self, kartu):
        kombinasi = [] #inisiasi kombinasi
        for i in range(1, len(kartu) + 1):
            for comb in itertools.combinations(kartu, i):
                kombinasi.append(comb) #menyatukan
        return kombinasi

    def brute_force_play(self):
        pemain_kartu = self.pemain[self.giliran]
        semua_kombinasi_kartu = self.semua_kombinasi(pemain_kartu) #membuat semua kombinasi kombinasi yang mungkin
        gerakan_valid = [komb for komb in semua_kombinasi_kartu if self.bisa_dilakukan(komb, self.tumpukan_terakhir)] #dibandingkan dengan kartu yang ada di tumpukan
        if not gerakan_valid:
            return [] #return kosong kalau gak valid
        gerakan_terbaik = min(gerakan_valid, key=lambda x: self.values.index(x[0][0])) #gerakan terkecil adalah gerakan terbaik
        return gerakan_terbaik

    def mainkan(self):
        while all(len(pemain) > 0 for pemain in self.pemain):
            gerakan = self.brute_force_play()
            if gerakan:
                self.tumpukan_terakhir = gerakan
                for kartu in gerakan:
                    self.pemain[self.giliran].remove(kartu)
                print(f"Pemain {self.giliran + 1} memainkan: {gerakan}")
            else:
                print(f"Pemain {self.giliran + 1} melewati giliran.")
                self.tumpukan_terakhir = []

            self.giliran = (self.giliran + 1) % 4

        pemenang = [i for i, pemain in enumerate(self.pemain) if len(pemain) == 0][0]
        print(f"Pemain {pemenang + 1} memenangkan permainan!")

# Inisialisasi permainan dan hitung waktu eksekusi
start_time = time.time()
permainan = BigTwo()
permainan.mainkan()
end_time = time.time()

print(f"Lama eksekusi: {end_time - start_time} detik")
