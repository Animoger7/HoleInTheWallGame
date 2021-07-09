using System.Collections;
using UnityEngine;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using System.Text;
using UnityEngine.SceneManagement;

public class HoleInTheWallGame: MonoBehaviour
{
    //Sound effects
    public AudioSource losing_sound;
    public AudioSource bomb_sound;

    //Visual effects
    public GameObject explosion_effect;

    //For connecting with python
    TcpClient client;
    TcpListener listener;
    public string connectionIP = "127.0.0.1";
    public int connectionPort = 25001;
    bool running;
    Thread mThread;
    NetworkStream nwStream;

    /*To control the dummy character*/
    //Root of the other bone transformatons
    private Transform hips;

    //Upper Body related transforms and initalizations.
    private Transform B_upper_arm_L, B_upper_arm_R, B_forearm_L, B_forearm_R;
    private Transform init_B_upper_arm_L, init_B_upper_arm_R, init_B_forearm_L, init_B_forearm_R;

    //Lower Body related transforms and initalizations.
    private Transform B_thigh_L, B_thigh_R, B_shin_L, B_shin_R, toe_L, toe_R;
    private Transform init_B_thigh_L, init_B_thigh_R, init_B_shin_L, init_B_shin_R;
    private Transform B_foot_L;
    private Transform B_foot_R;

    private Quaternion init_B_foot_L_rotation,init_B_foot_R_rotation;
    //Will hold the data of the coordinates recieved from python
    private string dataReceived = "";

    /* These are some play related variables to improve the user experience*/
    private float timeRemaining = 0;
    private bool firstCollisionTriggered = false;
    private float radius = 10f;
    private float force = 70f;

    public static int lifes_left = 3;

    void Start()
    {
        GameObject skeleton_prefab = GameObject.FindGameObjectWithTag("Dummy");//The root
        hips = skeleton_prefab.transform.GetChild(0);

        //Upper body init
        B_upper_arm_L = hips.GetChild(0).GetChild(0).GetChild(0).GetChild(1).GetChild(0);
        B_upper_arm_R = hips.GetChild(0).GetChild(0).GetChild(0).GetChild(2).GetChild(0);
        init_B_upper_arm_L = B_upper_arm_L.transform;
        init_B_upper_arm_R = B_upper_arm_R.transform;

        B_forearm_L = B_upper_arm_L.GetChild(0);
        B_forearm_R = B_upper_arm_R.GetChild(0);
        init_B_forearm_L = B_forearm_L.transform;
        init_B_forearm_R = B_forearm_R.transform;

        //Lower body init
        B_thigh_L = hips.GetChild(1);
        B_thigh_R = hips.GetChild(2);

        init_B_thigh_L = B_thigh_L.transform;
        init_B_thigh_R = B_thigh_R.transform;

        B_shin_L = B_thigh_L.GetChild(0);
        B_shin_R = B_thigh_R.GetChild(0);
        init_B_shin_L = B_shin_L.transform;
        init_B_shin_R = B_shin_R.transform;

        B_foot_L = B_shin_L.GetChild(0);
        B_foot_R = B_shin_R.GetChild(0);
        
        init_B_foot_L_rotation = B_shin_L.GetChild(0).rotation;
        init_B_foot_R_rotation = B_shin_R.GetChild(0).rotation;

        toe_L = B_shin_L.GetChild(0).GetChild(0);
        toe_R = B_shin_R.GetChild(0).GetChild(0);


        ThreadStart ts = new ThreadStart(GetInfo);
        mThread = new Thread(ts);
        mThread.Start();
        Time.timeScale = 0f;

    }

    private void Awake()
    {
        lifes_left = 3;
        firstCollisionTriggered = false;
        timeRemaining = 0;
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("Wall"))
        {
            if (timeRemaining <= 0)
            {
                lifes_left--;
                PathSpawner.wall_counter--;
                timeRemaining = 2;// To avoid several explosions
                firstCollisionTriggered = true;
                if (lifes_left > 0)
                {
                    explosion_effect.transform.localScale *= 5;

                    StartCoroutine(do_explosion(collision, 0f));
                }
                else
                {
                    if (lifes_left == 0)
                    {
                        CharacterMovement.gameOver();
                        CameraFollowPlayer.gameOver();
                        losing_sound.Play();
                        StartCoroutine(do_explosion(collision, 2.5f));

                    }
                }
            }
        }

    }
    private IEnumerator do_explosion(Collision collision, float delayTime)
    {
        yield return new WaitForSeconds(delayTime);
        bomb_sound.Play();
        foreach (Transform wall_brick in collision.gameObject.transform.parent.transform)
        {
            if (!wall_brick.CompareTag("bomb"))
            {
            Instantiate(explosion_effect, wall_brick.position, wall_brick.rotation);

            wall_brick.GetComponent<Rigidbody>().constraints = RigidbodyConstraints.None;
            }
            else
            {
                wall_brick.GetComponent<Rigidbody>().constraints = RigidbodyConstraints.None;
                Debug.Log(wall_brick.position+" "+wall_brick.rotation);
                Instantiate(explosion_effect, wall_brick.position, wall_brick.rotation);
                Collider[] colliders = Physics.OverlapSphere(wall_brick.position, radius);
                foreach(Collider neabyObject in colliders)
                {
                    Rigidbody rb = neabyObject.GetComponent<Rigidbody>();
                    if (rb != null && !rb.CompareTag("background") && !rb.CompareTag("MaleDummy"))
                        {
                        rb.GetComponent<Rigidbody>().AddExplosionForce(force, wall_brick.position, radius);
                        }
                }
            if(lifes_left==0)
            {
                yield return new WaitForSeconds(1.25f);
                listener.Stop();
                SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
            }
        }

        }
        }

    void Update()
    {
        Time.timeScale = 1f; 
        if (firstCollisionTriggered)
        {
            if (timeRemaining > 0)
            {
                //to avoid several collisions
                timeRemaining -= Time.deltaTime; // To avoid several explosions
            }
            else
            {
                if(lifes_left > 0)
                {
                    UpdateGameTransforms();
                }

            }
        }
        else
        {
            //Enter here till you collide for the first time
            UpdateGameTransforms();

        }
    }
    float calculate_angles_between_2_vectors(string[] landmark_1, string[] landmark_2, Vector2 baseVec)
    {

        Vector2 start = new Vector2(float.Parse(landmark_1[0]), float.Parse(landmark_1[1]));
        Vector2 end = new Vector2(float.Parse(landmark_2[0]), float.Parse(landmark_2[1]));
        Vector2 direction = end - start;
        direction.Normalize();
        float angle = Vector2.SignedAngle(direction, Vector2.right);
        angle = angle * -1;
        return angle;
    }


    void UpdateGameTransforms()
    {

        if (dataReceived != "")
        {

            string[] landmarks = dataReceived.Split('#');

            B_upper_arm_L.transform.eulerAngles = new Vector3(init_B_upper_arm_L.rotation.x, init_B_upper_arm_L.rotation.y, calculate_angles_between_2_vectors(landmarks[0].Split(','), landmarks[1].Split(','), Vector2.right));
            B_forearm_L.transform.eulerAngles = new Vector3(init_B_forearm_L.rotation.x, init_B_forearm_L.rotation.y, calculate_angles_between_2_vectors(landmarks[1].Split(','), landmarks[2].Split(','), Vector2.right));

            B_upper_arm_R.transform.eulerAngles = new Vector3(init_B_upper_arm_R.rotation.x, init_B_upper_arm_R.rotation.y, calculate_angles_between_2_vectors(landmarks[3].Split(','), landmarks[4].Split(','), Vector2.right));
            B_forearm_R.transform.eulerAngles = new Vector3(init_B_forearm_R.rotation.x, init_B_forearm_R.rotation.y, calculate_angles_between_2_vectors(landmarks[4].Split(','), landmarks[5].Split(','), Vector2.right));

            float leg_bending_left = calculate_angles_between_2_vectors(landmarks[6].Split(','), landmarks[7].Split(','), Vector2.right);
            B_thigh_L.transform.eulerAngles = new Vector3(init_B_thigh_L.rotation.x, init_B_thigh_L.rotation.y, leg_bending_left);
            B_shin_L.transform.eulerAngles = new Vector3(init_B_shin_L.rotation.x, init_B_shin_L.rotation.y, calculate_angles_between_2_vectors(landmarks[7].Split(','), landmarks[8].Split(','), Vector2.right));

            float leg_bending_right = calculate_angles_between_2_vectors(landmarks[9].Split(','), landmarks[10].Split(','), Vector2.right);
            B_thigh_R.transform.eulerAngles = new Vector3(init_B_thigh_R.rotation.x, init_B_thigh_R.rotation.y, leg_bending_right);
            B_shin_R.transform.eulerAngles = new Vector3(init_B_shin_R.rotation.x, init_B_shin_R.rotation.y, calculate_angles_between_2_vectors(landmarks[10].Split(','), landmarks[11].Split(','), Vector2.right));

            float height_diff = Mathf.Max(hips.position.y - toe_L.position.y, hips.position.y - toe_R.position.y);

            B_foot_L.rotation = init_B_foot_L_rotation;
            B_foot_R.rotation = init_B_foot_R_rotation;

            hips.position = new Vector3(hips.position.x, 5.960464e-09f + height_diff, hips.position.z);
        }
    }

    void GetInfo()
    {
        listener = new TcpListener(IPAddress.Any, connectionPort);
        listener.Start();

        client = listener.AcceptTcpClient();

        running = true;
        while (running)
        {
            getPoseCoords();
        }
        listener.Stop();
    }

    void getPoseCoords()
    {
        nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
        dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string
    }

    private void OnDestroy()
    {
        if(mThread!=null)
        {
            mThread.Abort();
        }
    }
}