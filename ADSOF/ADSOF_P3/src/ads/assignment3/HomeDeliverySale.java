package ads.assignment3;

/**
*
* Used for calculating additional charges from Sale
* 
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class HomeDeliverySale extends Sale {
	private double shipping;
	
	/**
	 * calculates the shipping on creation
	 * @param bought
	 */
	public HomeDeliverySale(Appliance bought) {
		super(bought);
		shipping = super.bought.calculateShipping();
		total = super.bought.getBasePrice() - super.discount + shipping;
	}
	/**
	 * calculates the shipping on creation
	 * @param boughtsuper.bought.getBasePrice()
	 * @param returned
	 */
	public HomeDeliverySale(Appliance bought, Appliance returned) {
		super(bought, returned);
		shipping = super.bought.calculateShipping();
		total = super.bought.getBasePrice() - super.discount + shipping;
	}
	
	
	@Override
	public String getTicket() {
		return toString() + String.format("Shipping Cost:                 %-7.2f Euros", shipping) + String.format("\nTOTAL:                         %-7.2f Euros", super.total) + "\n";

	}
	

}
