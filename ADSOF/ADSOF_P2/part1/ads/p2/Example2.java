package ads.p2;

import ads.p2.billing.*;

public class Example2 {
	public static void main(String args[]) {
		Article a3 = new Book(940111, "UML", 15, "Textbook");
		Article a4 = new Book(940607, "Classic readings", 10, "Collection");
		Book a5 = new Book(940607, "Fifty fifty", 3.25, "Unclassified");
		Tobacco a6 = new Tobacco(690023, "Marlboro", 1.75);

		int cant = 2;
		System.out.println(cant + " units of " + a3 + " Final price: " + a3.totalPrice(cant));
		cant = 5;
		System.out.println(cant + " units of " + a4 + " Final price: " + a4.totalPrice(cant));
		cant = 4;
		System.out.println(cant + " units of " + a5 + " Final price: " + a5.totalPrice(cant));
		cant = 1;
		System.out.println(cant + " units of " + a6 + " Final price: " + a6.totalPrice(cant));
	}
}
