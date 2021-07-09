using UnityEngine;
public class CameraFollowPlayer : MonoBehaviour
{
    public Transform character;
    public GameObject background;

    Vector3 offset_main;
    //public GameObject webCam;
    //Vector3 offset_web_cam;

    private static bool gameOverMode = false;
    private float gameover_camera_moving_factor = 1;
    // Start is called before the first frame update
    void Start()
    {
        gameOverMode = false;
        offset_main = transform.position - character.position;
        //offset_web_cam= webCam.transform.position - character.position;
    }

    // Update is called once per frame
    void Update()
    {
        if(!gameOverMode)
        {
            //Update Main Camera Position
            Vector3 targetPos = character.position + offset_main;
            targetPos.x = 0;
            transform.position = targetPos;

            //Update WebCam Position
            /*targetPos = character.position + offset_web_cam;
            targetPos.x = -0.67f;
            webCam.transform.position = targetPos;*/

            targetPos.x = -50.5f;
            targetPos.y = 70;
            targetPos.z += 200;

            background.transform.position = targetPos;
        }
        else
        {
            //For the camera zoom out effect at the end.
            Vector3 targetPos = character.position - (offset_main*0.11f* gameover_camera_moving_factor);
            if(gameover_camera_moving_factor<6)
            {
                gameover_camera_moving_factor += 0.025f;
            }
            targetPos.x = 0;
            targetPos.y = 16.5f;
            transform.position = targetPos;
            transform.eulerAngles = new Vector3(0, 180, 0);
        }
    }

    public static void gameOver()
    {
        gameOverMode = true;
    }
}
