using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class audio : MonoBehaviour
{
    AudioSource audioSource;
    public float pitchDividerHigherDeeper = 4000;
    public float minPitch = 0.1f, maxPitch = 2.8f;
    private float pitchFromCar;

    public float deltaJump = 0.05f;
    private float tempPitch;
    public CarController MyCarController;
    // Start is called before the first frame update
    void Start()
    {
        MyCarController = GetComponent<CarController>();
        audioSource = GetComponent<AudioSource>();
        audioSource.pitch = minPitch;
    }

    // Update is called once per frame
    void Update()
    {
        
        pitchFromCar = MyCarController.engineRPM/pitchDividerHigherDeeper;
        if (pitchFromCar < minPitch) tempPitch = minPitch;
        else if (pitchFromCar > maxPitch) tempPitch = maxPitch;
        else tempPitch = pitchFromCar;

        audioSource.pitch = Mathf.Lerp(audioSource.pitch, tempPitch, deltaJump);
        //audioSource.pitch = tempPitch;

    }
}