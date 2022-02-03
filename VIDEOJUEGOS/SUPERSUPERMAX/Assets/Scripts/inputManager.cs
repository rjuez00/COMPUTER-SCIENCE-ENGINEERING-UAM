using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class inputManager : MonoBehaviour
{

    public enum driver {
        keyboard,
        AI,
        mobile,
        pursuitAI,
        noDriver
    }

    [SerializeField] public driver driveController;
    [HideInInspector] public float vertical;
    [HideInInspector] public float horizontal;
    [HideInInspector] public bool handbrake;
    [HideInInspector] public bool driftbutton;
    [HideInInspector] public bool boosting;
    [HideInInspector] public bool gearUp;
    [HideInInspector] public bool gearDown;
    public bool racemodeAI = false;
    public List<Transform> nodes = new List<Transform>();

    [Range(0, 10)] public int AIdistanceOffset = 2;
    [Range(0, 5)] public int AIsteerForce = 3;
    [Range(0.2f,1.0f)] public float AIacceleration = 1;

    private float minimum_collision_distance = 6f;

    public trackWaypoints waypoints;
    private GameObject npcsconjunto;
    public List<GameObject> npcs = new List<GameObject>();
    public Transform currentWaypoint;


    private void Awake(){
        if (racemodeAI)
        {
            waypoints = GameObject.FindGameObjectWithTag("path").GetComponent<trackWaypoints>();
            nodes = waypoints.nodes;
            currentWaypoint = nodes[0];

            npcsconjunto = GameObject.Find("npcs");

            for (int i = 0; i < npcsconjunto.transform.childCount; i++)
            {
                npcs.Add(npcsconjunto.transform.GetChild(i).gameObject);
            }
        }
    }


    private void FixedUpdate() {
        switch (driveController)
        {
            case driver.AI: AIDrive();
                break;
            case driver.keyboard: keyboardDrive();
                break;
            case driver.pursuitAI: pursuitDrive();
                break;
            case driver.noDriver:
                break;
        }

        if (racemodeAI)
        {
            calculateDistanceOfWaypoints();
        }
    }
   

    private void keyboardDrive()
    {

        


        vertical = Input.GetAxis("Vertical");
        //Debug.Log(vertical);
        horizontal = Input.GetAxis("Horizontal");
        handbrake = Input.GetKey(KeyCode.LeftControl);
        driftbutton = (Input.GetAxis("Jump") != 0) ? true : false;
        
        if (Input.GetKey(KeyCode.LeftShift)) boosting = true; else boosting = false;
        if (Input.GetKey(KeyCode.E)) gearUp = true; else gearUp = false;
        if (Input.GetKey(KeyCode.Q)) gearDown = true; else gearDown = false;
        if (Input.GetKey(KeyCode.R))
        {
            string sceneName = SceneManager.GetActiveScene().name;
            if (!(sceneName.Contains("Menu") || sceneName.Contains("Loading") || sceneName.Contains("awake")))
            {
                SceneLoader.LoadLevel(sceneName);
            }
            
        }

        if (Input.GetKey(KeyCode.Escape))
        {
            string sceneName = SceneManager.GetActiveScene().name;
            if ((sceneName.Contains("Menu") || sceneName.Contains("Loading") || sceneName.Contains("awake")))
            {
                return;
            }
            else if (sceneName.Contains("Lobby") == true)
            {
                Application.Quit();
            }

            else
            {
                SceneLoader.LoadLevel("Lobby");
            }



        }




        //CHEAT CODE
        if (Input.GetKey(KeyCode.O)) {
            Debug.Log("Añadiendo 1000 coins");
            PlayerPrefs.SetInt("coins", PlayerPrefs.GetInt("coins") + 1000); 
        }




}

    private void AIDrive()
    {
        vertical = AIacceleration;
        AISteer();
    }


    private void pursuitDrive()
    {
        vertical = AIacceleration;
        pursuitSteer();
    }


    public GameObject toPursuit;
    private void pursuitSteer()
    {
        vertical = AIacceleration;


        bool override_waypoint = getClosestNPC(out Vector3 direccion_a_coche);

        override_waypoint = false;

        Vector3 steerVector;
        if (override_waypoint == true)
        {
            Debug.Log("EVITANDO ACCIDENTe");
            Debug.Log(direccion_a_coche);
            steerVector = direccion_a_coche;
        }
        else steerVector = toPursuit.transform.position;


        Vector3 relative = transform.InverseTransformPoint(steerVector);



        relative /= relative.magnitude;

        horizontal = (relative.x / relative.magnitude) * AIsteerForce;
    }



    // Start is called before the first frame update
    void Start()
    {
        toPursuit = GameObject.FindGameObjectWithTag("Vehicle");
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private Transform tempWaypoint;
    private void calculateDistanceOfWaypoints(){
        Vector3 position = gameObject.transform.position;
        float distance = Mathf.Infinity;

        
        for (int i = 0; i< nodes.Count-AIdistanceOffset; i++){
            Vector3 difference = nodes[i].transform.position - position;
            float currentDistance = difference.magnitude;
            if(currentDistance < distance) {
                tempWaypoint = nodes[ (i+AIdistanceOffset) % nodes.Count ];
                distance = currentDistance;
            }
        }


        currentWaypoint = tempWaypoint;
    }

    public bool isAvoidingCars = true;

    private void AISteer()
    {

        bool override_waypoint = getClosestNPC(out Vector3 direccion_a_coche);
        //Debug.Log(direccion_a_coche);
        
        
        Vector3 relative = transform.InverseTransformPoint(currentWaypoint.transform.position);

        if (override_waypoint == true)
        {
            Debug.Log("EVITANDO ACCIDENTe");
            Debug.Log(direccion_a_coche);
            relative = direccion_a_coche;
        }

        relative /= relative.magnitude;
        
        horizontal = (relative.x / relative.magnitude) * AIsteerForce;
    }



    private bool getClosestNPC(out Vector3 direccion_a_coche)
    {

        float distance;
        GameObject npc;


      
        npc = null;
        distance = Mathf.Infinity;

        for (int i = 0; i < npcs.Count; i++)
        {
    
            float tempdistance = Vector3.Distance(transform.position, npcs[i].transform.position);
            if (tempdistance < distance)
            {
                if(transform.position != npcs[i].transform.position)
                {
                    distance = tempdistance;
                    npc = npcs[i];
                }
                
            }
        }


        if (distance > minimum_collision_distance)
        {
            direccion_a_coche = Vector3.zero;
            return false;
        }
        direccion_a_coche = npc.transform.position - transform.position;
        direccion_a_coche.x = direccion_a_coche.x * -1;
        return true;
    }
    


    private void OnDrawGizmos(){
        if (racemodeAI)
        {
            Gizmos.DrawWireSphere(currentWaypoint.position, 3);
        }
    }



}
