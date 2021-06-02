package ads.assignment3;
import java.util.*;

/**
*
* Used for getting tickets for sales
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class Sale {
	private static ArrayList<Sale> history = null;
	/**
	 * bought appliance
	 */
	protected Appliance bought;
	/**
	 * returned by customer if it doenst return anything it will be null
	 */
	protected Appliance returned= null;
	/**
	 * discount applied to the appliance sale
	 */
	protected double discount = -1;
	/** 
	 * total price of the appliance sale
	 */
	protected double total = -1;
	
	/**
	 * constructor for buying without returning any item
	 * @param bought
	 */
	public Sale(Appliance bought) {
		this.bought = bought;
		if(history == null) history = new ArrayList<Sale>();
		discount = getDiscount();
		total = bought.getBasePrice() - discount;
		history.add(this);
		
		Stock stock = Stock.getInstance();
		stock.reduceStock(bought);
		
	}
	
	/**
	 * constructor for buying and returning items
	 * @param bought
	 * @param returned
	 */
	public Sale(Appliance bought, Appliance returned) {
		this.bought = bought;
		this.returned = returned;
		if(history == null) history = new ArrayList<Sale>();
		discount = getDiscount();
		total = bought.getBasePrice() - discount;
		history.add(this);
		
		Stock stock = Stock.getInstance();
		stock.reduceStock(bought);
		stock.addStock(returned);
	}

	/**
	 * calculates discount according to energy efficiency of the returned and bought items
	 * @return discount
	 */
	protected double getDiscount() {
		if(returned == null) {
			return 0;
		}
		
		if(returned.getEnergy() == EnergyEfficiency.UNKNOWN) {
			return 10;
		}
		
		double difference = returned.getEnergy().value() - bought.getEnergy().value();
		if(difference>0){
			return (difference*15 + 25);
		}
		if(difference<0) {
			return (difference*5 +25);
		}

		return 25;
	}
	
	
	public String toString() {
		return "--------------------------------------------\n" +
		"Sold Product: " + bought.toString() + " Euros"+
		"\n--------------------------------------------\n"      +
		String.format("Product price:                 %-7.2f Euros\n", bought.getBasePrice()) +
		String.format("Shipping discount:             %-7.2f Euros", discount) + "\n";
	}
	
	/**
	 * gets full info of the sale
	 * @return string
	 */
	public String getTicket() {
		return toString() + String.format("TOTAL:                         %-7.2f Euros", total)  + "\n";

	}
	
	/**
	 * gets the last sale constructed
	 * @return sale
	 */
	static public Sale last() {
		if(history.size()==0) return null;
		return history.get(history.size()-1);
	}

	/**
	 * cancels the last sale constructed
	 * @return sale
	 */
	static public Sale cancel() {
		if(history.size()==0) return null;
		Sale removed = history.get(history.size()-1);
		history.remove(history.size()-1);
		
		Stock stock = Stock.getInstance();
		stock.addStock(removed.bought);
		if(removed.returned != null) stock.reduceStock(removed.returned);
		
		return removed;
	}
	
	/**
	 * returns a sale summary with only the total cost
	 * @return string with the summary
	 */
	static public String salesSummary() {
		StringBuilder completestring = new StringBuilder("\nSALES SUMMARY:\n");
		for(Sale mySale: history) {
			completestring.append(     String.format("TOTAL:%1$30s\n", String.format("%-7.2f Euros", mySale.total)   )    );
		}
		
		
		return completestring.toString();
	}
	
	/**
	 * sets a min for filtering the sales
	 * @param min
	 * @return string with the summary
	 */
	static public String salesSummary(int min) {
		StringBuilder completestring = new StringBuilder("\nSALES SUMMARY:\n");
		for(Sale mySale: history) {
			if(mySale.total < min) continue;
			completestring.append(     String.format("TOTAL:%1$30s\n", String.format("%-7.2f Euros", mySale.total)   )    );
		}
		
		
		return completestring.toString();
	}
	
	/**
	 * sets a filter for the brand
	 * @param filter
	 * @return string with the summary
	 */
	static public String salesSummary(String filter) {
		StringBuilder completestring = new StringBuilder("\nSALES SUMMARY:\n");
		for(Sale mySale: history) {
			if(mySale.bought.getBrand().contains(filter) == false ) continue;
			completestring.append(     String.format("TOTAL:%1$30s\n", String.format("%-7.2f Euros", mySale.total)   )    );
		}
		
		
		return completestring.toString();
	}
	
}



