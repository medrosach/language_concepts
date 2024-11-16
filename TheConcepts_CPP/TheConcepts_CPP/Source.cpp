#include <iostream>
#include <Windows.h>
#include <limits>
#include <array>
#include <map>
#include <functional>
#include <variant>
#include <string>

using namespace std;

#pragma region The Concepts Implementation

#pragma region Var Types
void VarTypes() {
	cout << "Char types:" << endl;
	cout << "char               : " << sizeof(char) << " bytes. " << endl;
	cout << "char16_t           : " << sizeof(char16_t) << " bytes. " << endl;
	cout << "char32_t           : " << sizeof(char32_t) << " bytes. " << endl;
	cout << "wchar_t            : " << sizeof(wchar_t) << " bytes. " << endl;

	cout << endl << "Signed ints:" << endl;
	cout << "char               : " << sizeof(char) << " bytes. -" << (1 << (sizeof(char) * 8) - 1) - 1 << " < X < " << (1 << (sizeof(char)*8)-1)-1 << endl;
	cout << "short              : " << sizeof(short) << " bytes. -" << (1 << (sizeof(short) * 8) - 1) - 1 << " < X < " << (1 << (sizeof(short) * 8) - 1) - 1 << endl;
	cout << "int                : " << sizeof(int) << " bytes. -" << (1 << (sizeof(int) * 8) - 1) - 1 << " < X < " << (1 << (sizeof(int) * 8) - 1) - 1 << endl;
	cout << "long               : " << sizeof(long) << " bytes. -" << (1 << (sizeof(long) * 8) - 1) - 1 << " < X < " << (1 << (sizeof(long) * 8) - 1) - 1 << endl;
	cout << "long long          : " << sizeof(long long) << " bytes. -" << (1 << (sizeof(long long) * 8) - 1) - 1 << " < X < " << (1 << (sizeof(long long) * 8) - 1) - 1 << endl;

	cout << endl << "Unsigned ints:" << endl;
	cout << "unsigned char      : " << sizeof(unsigned char) << " bytes. 0 < X < " << (1 << (sizeof(char) * 8)) - 1 << endl;
	cout << "unsinged short     : " << sizeof(unsigned short) << " bytes. 0 < X < " << (1 << (sizeof(short) * 8)) - 1 << endl;
	cout << "unsigned int       : " << sizeof(unsigned int) << " bytes. 0 < X < " << (1 << (sizeof(int) * 8)) - 1 << endl;
	cout << "unsignedlong       : " << sizeof(unsigned long) << " bytes. 0 < X < " << (1 << (sizeof(long) * 8)) - 1 << endl;
	cout << "unsigned long long : " << sizeof(unsigned long long) << " bytes. 0 < X < " << (1 << (sizeof(long long) * 8)) - 1 << endl;

	cout << endl << "Floating point (decimals):" << endl;
	cout << "float              : " << sizeof(float) << " bytes. " << numeric_limits<float>::min << " < X < " << numeric_limits<float>::max << endl;
	cout << "double             : " << sizeof(double) << " bytes. " << numeric_limits<double>::min << " < X < " << numeric_limits<double>::max << endl;
	cout << "long double        : " << sizeof(long double) << " bytes. " << numeric_limits<long double>::min << " < X < " << numeric_limits<long double>::max << endl;

	cout << endl << "Boolean:" << endl;
	cout << "bool               : " << sizeof(bool) << " bytes. " << numeric_limits<bool>::min << " < X < " << numeric_limits<bool>::max << endl;
}
#pragma endregion

#pragma region STL Array usage
void UsingArrays() {
	char c_Array[] = { 'a','b','c','d' };
	cout << "Letters: ";
	for (auto iterator = begin(c_Array); iterator != end(c_Array); ++iterator)
		cout << *iterator << " ";
	cout  << endl;

	cout << "Reverse iterating: ";
	for (auto i = rbegin(c_Array); i != rend(c_Array); ++i)
		cout << *i << " ";
	cout << endl;

	array<int, 10> container_array;
	cout << "Array empty? " << container_array.empty() << endl;
	cout << "Container array size: " << container_array.size() << endl;
	cout << "Container max size  : " << container_array.max_size() << endl;
	container_array.fill(33);
	cout << "Container array: ";
	for (auto i = container_array.begin(); i != container_array.end(); ++i)
		cout << *i << " ";
	cout << endl;
	cout << "Array empty? " << container_array.empty() << endl;
}
#pragma endregion

#pragma region Class inheritance stuff
class undead {
	int HP;
public:
	undead() : HP(1) {}
	undead(int h) : HP(h) { }

	bool damage(int dmg) {
		if (dmg < 0) {
			cout << "Healing ";
		}
		else {
			cout << "Dealing ";
		}
		cout << dmg << " damage" << endl;
		HP -= dmg;
		return HP <= 0;
	}

	void showHP() {
		cout << "Current HP: " << HP << endl;
	}

	void describe() {
		cout << "I am undead" << endl;
	}

	virtual void speak() {
		cout << "Death is overrated" << endl;
	}

	virtual void attack() = 0; // <<---- This makes this class abstract
};
class vampire : public undead {
public: 
	vampire() : undead(100) {}
	vampire(int h): undead(h) {}

	void describe() {
		cout << "I am a vampire" << endl;
	}

	virtual void speak() {
		cout << "Blood! Blood! I want your blood!" << endl;
	}

	void attack() {
		cout << "FANGS OUT!" << endl;
	}
};
class zombie : public undead {
public:
	zombie() : undead(10) {}
	zombie(int h) : undead(h) {}

	void describe() {
		cout << "I is zombie" << endl;
	}

	virtual void speak() {
		cout << "Braaaaains!" << endl;
	}

	void attack() {
		cout << "HAND SWIPE" << endl;
	}
};
class skeleton : public undead {
public:
	skeleton() : undead(5) {}
	skeleton(int h) : undead(h) {}

	//This must be defined for compilation
	void attack() {
		cout << "Bone Storm!" << endl;
	}
};

void classStuff() {
	//undead ghost; <<-- You cant instantiate an abstract class
	undead* u_ptr;
	vampire* v_ptr;
	zombie* z_ptr;
	vampire alucard;
	zombie rob;
	skeleton kk;

	cout << "alucard.describe(): ";
	alucard.describe();
	cout << "alucard.showHP(): ";
	alucard.showHP();
	cout << "alucard.attack(): ";
	alucard.attack();
	cout << "alucard.speak(): ";
	alucard.speak();

	cout << "rob.describe(): ";
	rob.describe();
	cout << "rob.showHP(): ";
	rob.showHP();
	cout << "rob.attack(): ";
	rob.attack();
	cout << "rob.speak(): ";
	rob.speak();

	z_ptr = &rob;
	cout << "z_ptr(rob)->describe(): ";
	z_ptr->describe();
	cout << "z_ptr(rob)->showHP(): ";
	z_ptr->showHP();
	cout << "z_ptr(rob)->attack(): ";
	z_ptr->attack();
	cout << "z_ptr(rob)->speak(): ";
	z_ptr->speak();

	v_ptr = &alucard;
	cout << "v_ptr(alucard)->describe(): ";
	v_ptr->describe();
	cout << "v_ptr(alucard)->showHP(): ";
	v_ptr->showHP();
	cout << "v_ptr(alucard)->attack(): ";
	v_ptr->attack();
	cout << "v_ptr(alucard)->speak(): ";
	v_ptr->speak();

	u_ptr = &rob;
	cout << "u_ptr(rob)->describe(): ";
	u_ptr->describe();
	cout << "u_ptr(rob)->showHP(): ";
	u_ptr->showHP();
	cout << "u_ptr(rob)->attack(): ";
	u_ptr->attack();
	cout << "u_ptr(rob)->speak(): ";
	u_ptr->speak();

	u_ptr = &alucard;
	cout << "u_ptr(alucard)->describe(): ";
	u_ptr->describe();
	cout << "u_ptr(alucard)->showHP(): ";
	u_ptr->showHP();
	cout << "u_ptr(alucard)->attack(): ";
	u_ptr->attack();
	cout << "u_ptr(alucard)->speak(): ";
	u_ptr->speak();

	u_ptr = &kk;
	cout << "u_ptr(kk)->speak(): ";
	u_ptr->speak();
	cout << "u_ptr(kk)->attack(): ";
	u_ptr->attack();
}
#pragma endregion

#pragma region Menu managment
struct menuItem {
	string desc;
	function<void()> func;

	menuItem(){}
	menuItem(string theDesc, function<void()> theFunc) : desc(theDesc), func(theFunc) {}
};

bool menuPrinter(map<int, menuItem> oMap) {
	int choice;
	system("cls");
	for (map<int, menuItem>::iterator i = oMap.begin(); i != oMap.end(); ++i) {
		cout << i->first << ")" << i->second.desc << endl;
	}
	cout << "Enter choice number: ";
	cin >> choice;
	system("cls");
	if (oMap.find(choice) != oMap.end()) {
		oMap[choice].func();
		return true;
	}
	cout << "Thank you for reviewing...";
	return false;
}

bool Menu() {
	map<int, menuItem> optionsMap;

	optionsMap[1] = menuItem("Var Types", VarTypes);
	optionsMap[2] = menuItem("Arrays with iterator", UsingArrays);
	optionsMap[3] = menuItem("Class inheritance and virtuals", classStuff);

	return menuPrinter(optionsMap);
}
#pragma endregion

#pragma endregion

int main() {
	while (Menu()) {
		system("pause");
	}
	return 0;
}