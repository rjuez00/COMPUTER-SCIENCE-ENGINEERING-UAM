using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;


public class CarController : MonoBehaviour{

    public int price = 1000;
    public bool unlockedInSelector = false;


    private GameManager manager;
    private inputManager IM;
    
    internal enum driveType
    {
        frontWheelDrive,
        rearWheelDrive,
        allWheelDrive
    };
    [SerializeField] private driveType drive;

    internal enum gearBox
    {
        automatic,
        manual
    };
    [SerializeField] private gearBox gearChange;

    [HideInInspector] public bool test; //engine sound boolean

    public AnimationCurve enginePower;

    [Range(200, 300)] public int maxKPH = 210;

    public float KPH; 

    public float radius = 6;
    public float motorForce = 800;
    public float brake = 20000;

    private GameObject centerOfMass;


    //prueba
    private float moveInput;
    private float turnInput;
    private float handbrakeInput;
    private float steeringAngle;
    private bool nitrusInput;
    public float wheelsRPM;
    public float maxRPM, minRPM;


    public WheelCollider[] wheels = new WheelCollider[4];
    public Transform[] transforms = new Transform[4];
    public float[] slip = new float[4];
    public bool reverse = false;
    public float engineRPM;
    public float smoothTime = 0.01f;
    public float[] gears;
    public int gearNum = 0;

    private float lastValue;
    public float DownForceValue = 50;

    private Rigidbody rigidbody;
    private void addDownForce()
    {
        rigidbody.AddForce(-transform.up * DownForceValue * rigidbody.velocity.magnitude);
    }







    private void calculateEnginePower() {
        wheelRPM();
        motorForce = enginePower.Evaluate(engineRPM) * moveInput;
        float velocity = 0.0f;
        
        
        float gearratio = gears[gearNum];
   
        engineRPM = Mathf.SmoothDamp(engineRPM, 1000 + (Mathf.Abs(wheelsRPM) * (gearratio)), ref velocity, smoothTime);


        if (engineRPM >= maxRPM)
        {
            test = (lastValue > engineRPM) ? true : false;
        }
        else
        {
            test = false;
        }
    }

    private void wheelRPM() {
        float sum = 0;
        int R = 0;
        for (int i = 0; i < 4; i++)
        {
            sum += wheels[i].rpm;
            R++;
        }
        wheelsRPM = (R != 0) ? sum / R : 0;


        if (wheelsRPM < -10 && !reverse)
        {
            reverse = true;
            manager.changeGear();
        }
        else if (wheelsRPM > -10 && reverse)
        {
            reverse = false;
            manager.changeGear();
        }

    }

    private bool isGrounded()
    {
        if (wheels[0].isGrounded && wheels[1].isGrounded && wheels[2].isGrounded && wheels[3].isGrounded)
            return true;
        else
            return false;
    }
    
    private GameObject wheelMeshes, wheelColliders;
    private void getObjects()
    {
        IM = GetComponent<inputManager>();
        rigidbody = GetComponent<Rigidbody>();
        manager = GameObject.FindGameObjectWithTag("GameManager").GetComponent<GameManager>();
        wheelColliders = gameObject.transform.Find("WheelColliders").gameObject;
        wheelMeshes = gameObject.transform.Find("WheelMeshes").gameObject;
        wheels[0] = wheelColliders.transform.Find("FLW").gameObject.GetComponent<WheelCollider>();
        wheels[1] = wheelColliders.transform.Find("FRW").gameObject.GetComponent<WheelCollider>();
        wheels[2] = wheelColliders.transform.Find("RLW").gameObject.GetComponent<WheelCollider>();
        wheels[3] = wheelColliders.transform.Find("RRW").gameObject.GetComponent<WheelCollider>();

        transforms[0] = wheelMeshes.transform.Find("FLW");
        transforms[1] = wheelMeshes.transform.Find("FRW");
        transforms[2] = wheelMeshes.transform.Find("RLW");
        transforms[3] = wheelMeshes.transform.Find("RRW");

        centerOfMass = GameObject.Find("mass");
        rigidbody.centerOfMass = centerOfMass.transform.localPosition;
    }




    private void shifter()
    {
        if (!isGrounded()) return;

        if (gearChange == gearBox.automatic)
        {   
            //automatic
            if (engineRPM > maxRPM && gearNum < gears.Length - 1 && !reverse)
            {
                gearNum++;
                manager.changeGear();
                
            }
            if (engineRPM < minRPM && gearNum > 0)
            {
                gearNum--;
                manager.changeGear();
            }
        }


        else
        {   //manual 
            if (IM.gearUp && gearNum < gears.Length - 1)
            {
                gearNum++;
                manager.changeGear();
            }
            if (IM.gearDown && gearNum > 0)
            {
                gearNum--;
                manager.changeGear();
            }
        }

        if(engineRPM < minRPM && gearNum > 0)
        {
            gearNum--;
            manager.changeGear();
        }

    }



    public void GetInput()
    {
        turnInput = IM.horizontal;
        moveInput = IM.vertical;
        if (maxKPH < KPH)
        {
            moveInput = 0.0f;
        }
        handbrakeInput = IM.handbrake ? 1.0f : 0.0f;
        nitrusInput = IM.boosting;
        //Debug.Log(Input.GetKey("Jump"));
    }

    public void Steer()
    {
        //steeringAngle = 20 * turnInput;
        //frontLeftWheel.steerAngle = steeringAngle;
        //frontRightWheel.steerAngle = steeringAngle;

        wheels[0].steerAngle = Mathf.Rad2Deg * Mathf.Atan(2.55f / (radius + (1.5f/2)))*turnInput;
        wheels[1].steerAngle = Mathf.Rad2Deg *  Mathf.Atan(2.55f / (radius + (1.5f / 2))) * turnInput;
    }

    public void Accelerate()
    {
        
        if (moveInput < 0)
        {
            motorForce = motorForce * -1;
        }
        if (drive == driveType.allWheelDrive)
        {
            for (int i = 0; i < wheels.Length; i++)
            {
                wheels[i].motorTorque = moveInput * motorForce / 4;
            }
        }
        if (drive == driveType.frontWheelDrive)
        {
            for (int i = 0; i < wheels.Length -2; i++)
            {
                wheels[i].motorTorque = moveInput * motorForce / 2;
            }
        }

        else
        {
            for (int i = 2; i < wheels.Length; i++)
            {
                wheels[i].motorTorque = moveInput * motorForce / 2;
            }
        }

        KPH = rigidbody.velocity.magnitude * 3.6f;   
    }
    //


    public void Break()
    {
        // Handbrake
        for (int i = 2; i < wheels.Length; i++)
        {
            wheels[i].brakeTorque = handbrakeInput * brake;
        }
       
    }

    public void UpdateWheelPoses()
    {
        for (int i = 0; i < wheels.Length; i++)
        {
       

            Vector3 wheelPos = transforms[i].position;
            Quaternion wheelRotationQuat = transforms[i].rotation;

            wheels[i].GetWorldPose(out wheelPos, out wheelRotationQuat);

            transforms[i].position = wheelPos;
            transforms[i].rotation = wheelRotationQuat;
        }
        
    }


    private void getFriction()
    {
        for(int i = 0; i< wheels.Length; i++)
        {
            WheelHit wheelHit;
            wheels[i].GetGroundHit(out wheelHit);
            slip[i] = wheelHit.sidewaysSlip;
        }
    }






    public float nitrusValue = 0;
    public bool nitrusFlag = false;

    public void activateNitrus()
    {
        if(maxKPH < KPH)
        {
            return;
        }

        if (nitrusInput && nitrusValue > -1)
        {
            nitrusValue -= Time.deltaTime / 1;
        }
        else
        {
            nitrusValue += (nitrusValue >= 1.5f) ? 0  : Time.deltaTime;
        }

        if (nitrusInput)
        {
            if (nitrusValue > 0)
            {
                //CarEffects.startNitrusEmitter();
                nitrusFlag = true;
                rigidbody.AddForce(transform.forward * 5000);
            }
            else nitrusFlag = false;
        }
        else
        {
            nitrusFlag = false;
        }
        //else CarEffects.stopNitrusEmitter();

    }



    



    public void FixedUpdate()
    {
        if (SceneManager.GetActiveScene().name == "awakeScene") return;
        getObjects();
        GetInput();
        addDownForce();
        Steer();
        Accelerate();
        Break();
        UpdateWheelPoses();
        getFriction();
        calculateEnginePower();
        shifter();
        activateNitrus();
        lastValue = engineRPM;

        if (isNPCinPursuit == true) scriptPursuitNPC();
        if (isBeingProsecutedinPursuit == true) scriptPursuitProsecuted();

    }









    public bool isNPCinPursuit;
    public bool isBeingProsecutedinPursuit;


    public void scriptPursuitNPC()
    {
        //aqui si me choco muestro explosion y me autodestruyo

        /*if (logica para saber si me he chocado o no)
        {
            //mostrar explosion
            Destroy(gameObject);
        }*/
    }

    public void scriptPursuitProsecuted()
    {
        //aquí si me chocan llamo a algun procedimiento de GameManager o lo que sea que para la partida y muestra el tiempo
        //muestro explosion
    }





}
