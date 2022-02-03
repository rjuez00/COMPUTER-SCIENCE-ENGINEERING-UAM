using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class GameManager : MonoBehaviour
{
    
    
    
    public GameObject[] policeVehicles;
    public float spawnPeriod = 2f;
    private float nextActionTime = 0.0f;
    public GameObject[] policeSpawnPoints;
    public bool pursuitMode;





    public CarController RR;
    public GameObject needle;
    private float startPosition = 223.19f, endPosition = -40f;
    private float desiredPosition;
    public Slider nitrusSlider;

    public Text kph;
    public Text gearNum;
    // Start is called before the first frame update

    public bool useChosenVehicle = true;
    public GameObject vehicleStartLocation;
    public vehicleList list;


    public GameObject pursuitExplosionEffect = null;


    void Awake()
    {

        if (useChosenVehicle == true)
        {
            vehicleStartLocation = GameObject.Find("startLocation");
            GameObject playerCar = Instantiate(list.vehicles[PlayerPrefs.GetInt("pointer")], vehicleStartLocation.transform.position, vehicleStartLocation.transform.rotation);
            if (pursuitMode == true) playerCar.GetComponent<CarController>().isBeingProsecutedinPursuit = true;
        }
        FindValues();
    }

    void FindValues(){
        RR = GameObject.FindGameObjectWithTag("Vehicle").GetComponent<CarController>();
        kph = GameObject.Find("car_hud/speedometer/kph").GetComponent<Text>();
        gearNum = GameObject.Find("car_hud/speedometer/gearNum").GetComponent<Text>();
        needle  = GameObject.Find("car_hud/speedometer/needle");
        nitrusSlider = GameObject.Find("car_hud/speedometer/nitro").GetComponent<Slider>();
    }


    // Update is called once per frame
    void FixedUpdate()
    {
        kph.text = RR.KPH.ToString("0");
        updateNeedle();
        nitrusUI();
        
    }


    public void updateNeedle()
    {
        desiredPosition = startPosition - endPosition;
        float temp = RR.engineRPM/7000;
        needle.transform.eulerAngles = new Vector3(0, 0, (startPosition - temp * desiredPosition));
    }
    public void nitrusUI()
    {
        nitrusSlider.value = (RR.nitrusValue / 2);
    }

    public void changeGear()
    {
        gearNum.text = (!RR.reverse) ? (RR.gearNum + 1).ToString() : "R";
    }


    void Update()
    {
        if (pursuitMode == true)
        {
            if (Time.time > nextActionTime)
            {
                nextActionTime = Time.time + spawnPeriod;
                spawnPoliceCar();
            }
        }
    }


    void spawnPoliceCar()
    {
        int idxPoliceToSpawn = Random.Range(0, policeVehicles.Length);
        int idxWhereToSpawn = Random.Range(0, policeSpawnPoints.Length);

        GameObject carInstantiated = Instantiate(policeVehicles[idxPoliceToSpawn], policeSpawnPoints[idxWhereToSpawn].transform.position, policeSpawnPoints[idxWhereToSpawn].transform.rotation);
        carInstantiated.GetComponent<CarController>().isNPCinPursuit = true;
        carInstantiated.tag = "NPCPursuit";
        carInstantiated.GetComponent<inputManager>().driveController = inputManager.driver.pursuitAI;


        carInstantiated.GetComponent<inputManager>().AIacceleration = Random.Range(0.5f, 1f);

        carInstantiated.GetComponent<inputManager>().AIsteerForce = Random.Range(2, 4);

        carInstantiated.AddComponent<CarExplodeOnCollision>();
        carInstantiated.GetComponent<CarExplodeOnCollision>().explosionEffect  = pursuitExplosionEffect;
    }
}
