#include <bits/stdc++.h>
using namespace std;

string decodeCaesar(string cipher, int key) {
	for (size_t i = 0; i < cipher.size(); ++i) {
		char &c = cipher[i];

		if (c >= 'a' && c <= 'z') {
			c = char((c - 'a' - key + 26) % 26 + 'a');
		} else if (c >= 'A' && c <= 'Z') {
			c = char((c - 'A' - key + 26) % 26 + 'A');
		}
	}
	return cipher;
}

string encodeCaesar(string plain, int key) {
	for (size_t i = 0; i < plain.size(); ++i) {
		char &c = plain[i];
        
		if (c >= 'a' && c <= 'z') {
			c = char((c - 'a' + key) % 26 + 'a');
		} else if (c >= 'A' && c <= 'Z') {
			c = char((c - 'A' + key) % 26 + 'A');
		}
	}
	return plain;
}

int main() {
	string cipher = "odroboewscdrolocdcwkbdmyxdbkmdzvkdpybwyeddrobo";

	for (int k = 1; k < 26; ++k) {
		cout << "Key = " << k << " Decoded Text - " << decodeCaesar(cipher, k) << endl;
	}

	string plain = decodeCaesar(cipher, 10);
	cout << "\nDecoded Text (using key 10): " << plain << endl;
	cout << "Encoded back (using key 10): " << encodeCaesar(plain, 10) << endl;

	return 0;
}
