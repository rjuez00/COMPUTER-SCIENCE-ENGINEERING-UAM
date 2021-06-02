package ads.assignment3;

import java.util.*;

public class Stock {
	private static Stock INSTANCE;
    private Hashtable<Appliance, Integer> stocks = new Hashtable<Appliance, Integer>();
    /*we made everything static in order to make it easy to pass the inventory to most classes
     * without adding arguments to methods*/
    private Stock() {}
    
    public static Stock getInstance() {
    	if(INSTANCE == null) INSTANCE = new Stock();
    	return INSTANCE;
    }	
    
    public void addStock(Appliance newappliance){
    	if(stocks.containsKey(newappliance) == true) {
    		int myStock = stocks.get(newappliance);
    		myStock = myStock +1;
    		stocks.put(newappliance, myStock);
    	}
    	else stocks.put(newappliance, 1);
    }
    
   public void reduceStock(Appliance oldappliance) {
    	if(stocks.containsKey(oldappliance) == true) {
    		int myStock = stocks.get(oldappliance);
    		myStock = myStock -1;
    		if(myStock==0){
    			stocks.remove(oldappliance);
    		}
    		else stocks.put(oldappliance, myStock);
    		
    	}
    }
    
    public void discontinueAppliance(Appliance discontinueapp) {
    	if(stocks.containsKey(discontinueapp) == false) return;
    	stocks.remove(discontinueapp);
    }
    
    /** 
	 * returns brand, model and baseprice
	 * @return String
	 */
	public String toString() {
		StringBuilder completestring = new StringBuilder("");
		completestring.append("|-----------------------------------------|\n");
		Set<Appliance> keyset = stocks.keySet();
		for (Appliance mystock: keyset) {
			completestring.append(String.format("|%-30s || STOCK:%d|\n", mystock, stocks.get(mystock)));
		}
		completestring.append("|-----------------------------------------|\n");
		return completestring.toString();
	}
	
    
    public String showStock() {
    	return toString();
    }
    
    public String showStock(Class <? extends Appliance> clase) {
    	StringBuilder completestring = new StringBuilder("");
		completestring.append("|-----------------------------------------|\n");
		Set<Appliance> keyset = stocks.keySet();
		for (Appliance mystock: keyset) {
			if(mystock.getClass() == clase)
				completestring.append(String.format("|%-30s || STOCK:%d|\n", mystock, stocks.get(mystock)));
		}
		completestring.append("|-----------------------------------------|\n");
		return completestring.toString();
    }
    

}
