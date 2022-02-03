using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using UnityEditor;


public class awakeManager : MonoBehaviour
{
    public Text fundings;
    public Text coinsText;
    public GameObject purchaseButton;

    



    public float rotateSpeed = 15;
    public Vector3 rotation;

    public GameObject toRotate;
    public int vehiclePointer = 0;
    public vehicleList listOfVehicles;

    public List<int> vehiclesUnlocked = new List<int>();



    public bool changingVehicle = false;
    private void FixedUpdate()
    {   if (changingVehicle == false) toRotate.transform.Rotate(Vector3.up * rotateSpeed * Time.deltaTime);
    }

    // Update is called once per frame
    private void Awake()
    {
        vehiclePointer = PlayerPrefs.GetInt("pointer");
        GameObject childObject = Instantiate(listOfVehicles.vehicles[vehiclePointer], Vector3.zero, toRotate.transform.rotation) as GameObject;
        childObject.transform.parent = toRotate.transform;
        coinsText.text = string.Format("{0:000000}", childObject.GetComponent<CarController>().price);
        fundings.text = string.Format("{0:000000000000}", PlayerPrefs.GetInt("coins"));




        loadUnlockedVehicles();


        checkCocheDesbloqueado(vehiclePointer);

    }


    private void loadUnlockedVehicles()
    {


        for (int i = 0; i < listOfVehicles.vehicles.Length; i++)
            vehiclesUnlocked.Add(PlayerPrefs.GetInt("vehiclesUnlocked_" + i));
    }


    private void saveUnlockedVehicles()
    {
        PlayerPrefs.SetInt("vehiclesUnlocked_count", vehiclesUnlocked.Count);
        for (int i = 0; i < vehiclesUnlocked.Count; i++)
            PlayerPrefs.SetInt("vehiclesUnlocked_" + i, vehiclesUnlocked[i]);
    }


    public void startButton()
    {

        if (checkCocheDesbloqueado(vehiclePointer) == false) return;

        saveUnlockedVehicles();
        PlayerPrefs.SetInt("pointer", vehiclePointer);
        SceneLoader.LoadLevel("Lobby");
    }



    public void rightButton()
    {
        changingVehicle = true;
        if (vehiclePointer < listOfVehicles.vehicles.Length - 1)
        {
            Destroy(GameObject.FindGameObjectWithTag("Vehicle"));
            vehiclePointer++;
            GameObject childObject = Instantiate(listOfVehicles.vehicles[vehiclePointer], Vector3.up*3, toRotate.transform.rotation) as GameObject;
            childObject.transform.parent = toRotate.transform;
            //getCarInfo();

            coinsText.text = string.Format("{0:000000}", childObject.GetComponent<CarController>().price);

            checkCocheDesbloqueado(vehiclePointer);

        }
        changingVehicle = false;



    }

    public void leftButton()
    {
        changingVehicle = true; 
        if (vehiclePointer > 0)
        {
            Destroy(GameObject.FindGameObjectWithTag("Vehicle"));
            vehiclePointer--;
            GameObject childObject = Instantiate(listOfVehicles.vehicles[vehiclePointer], Vector3.up * 3, toRotate.transform.rotation) as GameObject;
            Debug.Log(childObject);
            childObject.transform.parent = toRotate.transform;
            //getCarInfo();

            coinsText.text = string.Format("{0:000000}", childObject.GetComponent<CarController>().price);


            checkCocheDesbloqueado(vehiclePointer);

        }
        changingVehicle = false;


    }



    private bool checkCocheDesbloqueado(int index)
    {

        if(listOfVehicles.vehicles[index].GetComponent<CarController>().unlockedInSelector == true)
        {
            purchaseButton.SetActive(false);
            return true;
        }


        if (vehiclesUnlocked[index] == 0)
        {
            purchaseButton.SetActive(true);
            return false;
        }

       

        purchaseButton.SetActive(false);
        return true;
    }

    private void desbloquearCoche(int index)
    {
        vehiclesUnlocked[index] = 1;
        purchaseButton.SetActive(false);
    }


    public void compraCoche()
    {

        int currCoins = PlayerPrefs.GetInt("coins");
        currCoins -= listOfVehicles.vehicles[vehiclePointer].GetComponent<CarController>().price;
        if (currCoins < 0) return;


        PlayerPrefs.SetInt("coins", currCoins);
        fundings.text = string.Format("{0:000000000000}", PlayerPrefs.GetInt("coins"));

        desbloquearCoche(vehiclePointer);



    }


}
