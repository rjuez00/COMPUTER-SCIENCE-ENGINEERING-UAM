package ads.p2.billing;

/**
*
*  class to store the description of a Book an its specific discounts and types
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class Book extends Article {
    /*extra string to know the type*/
    private String type;
   /**
   * Builds an object book
   * @param id id of article
   * @param desc description of article
   * @param price base price without any discount
   * @param b_type type of the book
   */
    public Book(long id, String desc, double price, String b_type){
            super(id, desc, price);
            type = b_type;
    }
   /**
   * Returns book VAT
   * @return double with 4%vat
   */
    public double typeVAT(){ return 0.04;}
   /**
   * getter of type
   * @return string with type
   */
    public String get_type(){ return type;}
   /**
   * setter of type
   * @param b_type with type
   */
    public void set_type(String b_type){ type = b_type;}
   /**
   * Calculates the required discount for every type of book
   * @param units double with the cuantity
   * @return double with the amount to discount
   */
    public double discount(double units){
        if(type.equals("Textbook")) return super.getUnitPrice() * 0.15 * units;
        
        else if(type.equals("Collection")){
            if(units >= 3) return (super.getUnitPrice() * 0.5 * (units-2));
            else return 0.0;
        }
        else return 0.0;
    }
}