using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UpdateCoins : MonoBehaviour
{
    public GameObject instructions;
    public Text coinsText;
    public bool isLobby = false;

    private bool first_flag = false;

    void Start()
    {
        if (isLobby == true) instructions.SetActive(false);

        int firstTime = PlayerPrefs.GetInt("first_time");
        if (firstTime == 0)
        {
            PlayerPrefs.SetInt("coins", 1000);
            PlayerPrefs.SetInt("first_time", 1);
        }
        coinsText.text = string.Format("{0:000000000000}", PlayerPrefs.GetInt("coins"));


        int first_init = PlayerPrefs.GetInt("first_initialization");
        if (first_init == 0 & isLobby == true)
        {
            PlayerPrefs.SetInt("first_initialization", 1);
            instructions.SetActive(true);
            first_flag = true;

        }
    }



    private void Update()
    {
        if (isLobby == false) return;
        if (Input.GetKey(KeyCode.H))
        {
            instructions.SetActive(true);
            first_flag = false;
        }
        else if(first_flag == false)
        {
            instructions.SetActive(false);
        }
    }





}
