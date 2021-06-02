package ads.assignment3;

import java.util.ArrayList;

public class CanaryIslandsSale extends Sale {
	private static ArrayList<Sale> history = null;
	protected Appliance bought;
	protected Appliance returned= null;
	
	/**
	 * constructor for buying without returning any item
	 * @param bought
	 */
	public CanaryIslandsSale(Appliance bought) {
		super(bought);
		if(history == null) history = new ArrayList<Sale>();
		discount = getDiscount();
		total = bought.getBasePrice() - discount;
		history.add(this);
	}

	/**
	 * constructor for buying and returning items
	 * @param bought
	 * @param returned
	 */
	public CanaryIslandsSale(Appliance bought, Appliance returned) {
		super(bought, returned);
		if(history == null) history = new ArrayList<Sale>();
		discount = super.getDiscount();
		total = bought.getBasePrice() - discount;
		history.add(this);
	}
	
	@Override
	public String getTicket() {
		return toString() + String.format("TOTAL:                         %-7.2f Euros", total)  + "\n";

	}

}
