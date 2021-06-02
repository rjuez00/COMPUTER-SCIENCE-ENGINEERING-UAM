package ads.assignment3;

/**
*
* Used for calculating additional charges from Sale specially for Canary Islands
* 
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/

public class CanaryIslandsHomeDeliverySale extends Sale {
	private Double shipping;
	
	/**
	 * calculates the shipping on creation (returned appliances not available)
	 * @param bought
	 */
	public CanaryIslandsHomeDeliverySale(Appliance bought) {
		super(bought);
		shipping = super.bought.getBasePrice()*0.07;
		total = super.bought.getBasePrice() - super.discount + shipping;
	}
	
	@Override
	public String getTicket() {
		return toString() + String.format("Shipping Cost:                 %-7.2f Euros", shipping) + String.format("\nTOTAL:                         %-7.2f Euros", super.total) + "\n";

	}

}
