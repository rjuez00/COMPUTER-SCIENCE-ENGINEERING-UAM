/**
*
* This program checks if a number is prime and prints its previous primes and divisors.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/

import java.util.*;


public class Primes {
   // we use an ordered set, implemented by TreeSet   
   private SortedSet<Integer> primes= new TreeSet<>();
   // another ordered set for the divisors
   private int max=1;








   /**
    * Returns the Set of Primes
    * @return cache with calculated primes
    */
   public SortedSet<Integer> getPrimes(){
       return primes;
   }

    /**
    * Transforms to string class data
	* @return String representing this object
    */
	public String toString(){
       return "Primes up to "+ max+ " = "+primes;
    }



   /**
    * This method checks if "n" is prime by updating the set of Primes up to "n" and
    * checking if it is one of them
    * @param n value to check
    * @return if n is prime
    */
   public boolean isPrime(int n){
	   if (n<2) return false;
	   if (n>max) updatePrimes(n);
	   return primes.contains(n); /*it will be contained after updating primes*/
	}
  

   /**
    * This method calls checkPrime and adds it, if it is prime, for all 
    * numbers between max+1 and n. Updates max at the end.
    * @param n value to check
    */
   private void updatePrimes(int n){
       for (int i = max+1; i<=n; i++){
            if(checkPrime(i) == true) {primes.add(i);}
        }

        max=n;
   }


   /**
    * Checks if n is prime, assuming that the set of primes is updated with
    * all previous ones
    * @param n value to check
    * @return if n is prime
    */
   private boolean checkPrime(int n){
       boolean prime = true;

        if(n<2) return false;

        for(int i = 2; i <= (n/2); i++){ /*no number higher than n/2 will be a divisor of n*/
            if(n%i == 0) {
                prime = false;
                break;
            }
        }

        return prime;
   }




   /**
   * Calculates the prime divisors of the argument n
   * @param n value to operate
   * @return SortedSet with the divisors of "n"
   */
   public SortedSet<Integer> primeDivisors(int n){
    SortedSet<Integer> primedivisors= new TreeSet<>();
    Iterator<Integer> iterator = primes.iterator();
    updatePrimes(n); /*we update all the primes up to that number so that is included in the result*/

    while(iterator.hasNext()){
        Integer oneprime = iterator.next(); /*we iterate through the sortedset to check if*/
        if(n%oneprime == 0){                  /*one of the primes is a factor of the number*/
            primedivisors.add(oneprime);
        }
    }
    return primedivisors;
}






   /**
   * main takes the arguments and returns if they're primes, the primes up to them and their divisors
   * @param args A string array containing the command line arguments
   */
    public static void main(String[] args) {

        if(args.length < 1) {
            System.out.println("Expecting 1 or more arguments");
            return;
        }

        for(String s: args){
            System.out.println();
            int n = Integer.parseInt(s);
            Primes prime = new Primes();

            System.out.println("Is " + n + " a prime? " + prime.isPrime(n));
            System.out.println(prime.toString());
            System.out.println("Divisors of " + n + " = " + prime.primeDivisors(n));
        }

    }
}


