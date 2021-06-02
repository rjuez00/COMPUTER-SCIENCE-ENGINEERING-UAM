package rules.triggers;

/**
 * FunctionalInterface which must implement those Classes that can have triggerers (observers)
 *
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 * 
 * @param <T> the generic type
 */
public interface Observed<T> {
	void addTriggerer(TriggeredRule<?> triggerer);
}
