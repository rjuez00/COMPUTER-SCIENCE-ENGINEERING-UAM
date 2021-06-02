package ads.assignment3;

/**
*
* Used for calculating additional charges from Sale specially for Canary Islands
* 
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/

public class CanaryIslandsHomeDeliverySale extends HomeDeliverySale {
	
	/**
	 * calculates the shipping on creation (returned appliances not available)
	 * @param bought
	 */
	public CanaryIslandsHomeDeliverySale(Appliance bought) {
		super(bought);
	}
	
	@Override
	protected double obtainShipping() {
		return super.bought.getBasePrice()*0.07;
	}
	
	
	@Override
	public String getTicket() {
		return toString() + String.format("Shipping Cost:                 %-7.2f Euros", super.shipping) + String.format("\nTOTAL:                         %-7.2f Euros", super.total) + "\n";

	}

}
