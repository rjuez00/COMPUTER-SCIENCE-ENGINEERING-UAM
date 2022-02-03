using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;


[RequireComponent(typeof(AudioSource))]
public class Race : MonoBehaviour
{
    public Text positionTxt;
    public Text finishMsg;

    AudioSource endingMusic;

    public void Update()
    {
        positionTxt.text = string.Format("POS {0}/{1}", TrackCheckpoints.Instance.PlayerPosition, TrackCheckpoints.Instance.NumberOfCars);
    }

    public void EndRace()
    {

        if (TrackCheckpoints.Instance.PlayerPosition == 1)
        {
            finishMsg.text = string.Format("You finished the race in 1st position!", TrackCheckpoints.Instance.PlayerPosition);
        }
        else if (TrackCheckpoints.Instance.PlayerPosition == 2)
        {
            finishMsg.text = string.Format("You finished the race in 2nd position!", TrackCheckpoints.Instance.PlayerPosition);
        }
        else if (TrackCheckpoints.Instance.PlayerPosition == 3)
        {
            finishMsg.text = string.Format("You finished the race in 3rd position!", TrackCheckpoints.Instance.PlayerPosition);
        }
        else
        {
            finishMsg.text = string.Format("You finished the race in {0}th position!", TrackCheckpoints.Instance.PlayerPosition);
        }

        // Coin reward
        int currCoins = PlayerPrefs.GetInt("coins");
        int newCoins = Mathf.Max(1000 - 250 * (TrackCheckpoints.Instance.PlayerPosition - 1), 50);
        currCoins += newCoins;
        PlayerPrefs.SetInt("coins", currCoins);
        finishMsg.text += string.Format("\nYou won {0} coins!", newCoins);


        endingMusic = GetComponent<AudioSource>();
        endingMusic.Play(0);
        // Takes the Player to the lobby after a 5 second timer
        StartCoroutine(WaitAndLeave(5));
    }

    private IEnumerator WaitAndLeave(float waitTime)
    {
        yield return new WaitForSeconds(waitTime);
        SceneLoader.LoadLevel("Lobby");
    }

}
