/**
 * 
 */
package rules;

import java.util.function.Consumer;
import java.util.function.Predicate;

/**
 * The class of rules.
 *
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 * 
 * @param <T> the generic type
 */
public class Rule<T> {
	
	/** The name of the rule. */
	private String name;
	
	/** The description of the rule. */
	private String description;
	
	/** The Predicate when. */
	private Predicate<T> whencond;
	
	/** The Consume when. */
	private Consumer<T> execwhen;
	
	
	/**
	 * Instantiates a new rule.
	 *
	 * @param name the name
	 * @param description the description
	 */
	public Rule(String name, String description) {
		this.name = name;
		this.description = description;
	}

	/**
	 * Creating a new rule.
	 *
	 * @param <T> the generic type
	 * @param string the name
	 * @param string2 the description
	 * @return the rule
	 */
	public static <T> Rule<T> rule(String string, String string2) {
		return new Rule<T>(string, string2);
	}
	
	/**
	 * Rule When.
	 *
	 * @param whencond the whencond
	 * @return the rule
	 */
	public Rule<T> when(Predicate<T> whencond) {
		this.whencond = whencond;
		return this;
	}

	/**
	 * Rule Exec.
	 *
	 * @param execwhen the execwhen
	 * @return the rule
	 */
	public Rule<T> exec(Consumer<T> execwhen) {
		this.execwhen = execwhen;
		return this;
	}
	
	
	/**
	 * Gets the description.
	 *
	 * @return the description
	 */
	public String getDescription() {
		return description;
	}

	/**
	 * Gets the name.
	 *
	 * @return the name
	 */
	public String getName() {
		return name;
	}

	/**
	 * Gets the when Predicate.
	 *
	 * @return the when Predicate
	 */
	public Predicate<T> getWhen() {
		return whencond;
	}

	/**
	 * Gets the exec Consumer.
	 *
	 * @return the exec Consumer
	 */
	public Consumer<T> getExec() {
		return execwhen;
	}

	public void setDescription(String desc) {
		this.description = desc;
	}
}
