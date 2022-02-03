using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


[RequireComponent(typeof(AudioSource))]
public class Pursuit : MonoBehaviour
{
    // Singleton instance
    private static Pursuit instance = null;

    public Text timerText;
    public Text finishMsg;

    private bool updateTimer = true;

    GameObject playerCar = null;
    private float timer = 0.0f;
    private bool gameModeEnded = false;

    AudioSource endingMusic;

    public static Pursuit Instance
    {
        get
        {
            if (instance == null)
            {
                instance = FindObjectOfType<Pursuit>();
                if (instance == null)
                {
                    Debug.Log("Creacionando");
                    instance = new GameObject("Pursuit").AddComponent<Pursuit>();
                }
            }
            return instance;
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        playerCar = GameObject.FindGameObjectWithTag("Vehicle");
        playerCar.AddComponent<PlayerCollisionDetection>();
    }

    // Update is called once per frame
    void Update()
    {
        if (updateTimer)
        {
            timer += Time.deltaTime;

            int minutes = Mathf.FloorToInt(timer / 60);
            int seconds = Mathf.FloorToInt(timer - minutes * 60);
            int millis = Mathf.FloorToInt((timer - minutes * 60 - seconds) * 1000);
            timerText.text = string.Format("{0:00}:{1:00}.{2:000}", minutes, seconds, millis);
        }
    }

    public void EndPursuit()
    {
        if (!gameModeEnded)
        {
            gameModeEnded = true;
            updateTimer = false;

            int minutes = Mathf.FloorToInt(timer / 60);
            int seconds = Mathf.FloorToInt(timer - minutes * 60);
            int millis = Mathf.FloorToInt((timer - minutes * 60 - seconds) * 1000);
            finishMsg.text = string.Format("You lasted {0:00}:{1:00}.{2:000}", minutes, seconds, millis);

            // Coin reward
            int currCoins = PlayerPrefs.GetInt("coins");
            int newCoins = Mathf.RoundToInt(3.33333f * timer);
            currCoins += newCoins;
            PlayerPrefs.SetInt("coins", currCoins);
            finishMsg.text += string.Format("\nYou won {0} coins!", newCoins);

            endingMusic = GetComponent<AudioSource>();
            endingMusic.Play(0);
            StartCoroutine(WaitAndLeave(5));
        }
        
    }

    private IEnumerator WaitAndLeave(float waitTime)
    {
        yield return new WaitForSeconds(waitTime);
        SceneLoader.LoadLevel("Lobby");
    }

}
