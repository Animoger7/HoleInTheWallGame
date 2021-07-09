using UnityEngine;

public class PathSpawner : MonoBehaviour
{
    public GameObject groundTile;
    public GameObject[] walls = new GameObject[5];// T pose, Left , Right, hands up ,squat
    private GameObject[] wall_clones = new GameObject[3];
    Vector3 nextSpawnPoint;
    private int counter = 0;
    private static int sequence_index = 0;
    private int wall_index = 0;
    public static int wall_counter = -1;
    public static int max_wall_counter = 0;

    //Displays the score and lives left while still in game
    public TextMesh score;

    public void spawnObjects()
    {
        //Spawn Tile
        GameObject temp=Instantiate(groundTile, nextSpawnPoint, Quaternion.identity); // Quaternion.identity= No rotation
        
        if(counter%4==3 )//To put a wall every 4'th tile only.
        {
            wall_counter++;
            choose_sequence();
            //Spawn Wall
            Vector3 spawnPos = new Vector3(0.5f,17, nextSpawnPoint.z);
            wall_clones[counter%3] =  Instantiate(walls[wall_index], spawnPos, Quaternion.identity);
            if (wall_counter > max_wall_counter)
            {
                max_wall_counter = wall_counter;
            }
            score.text = "Score: " + wall_counter+"\nLives: "+ HoleInTheWallGame.lifes_left;
            MAINMENU.UpdateScoreText(wall_counter, max_wall_counter);

        }
        nextSpawnPoint = temp.transform.GetChild(1).transform.position;
        counter++;
    }

    public void destroy_current_wall_clone()
    {
        if(counter%4==0)
        {
            Destroy(wall_clones[(counter - 2) % 3], 2f);
        }
    }

    // Start is called before the first frame update
    private void Start()
    {

        //random seed 
        sequence_index = Random.Range(0, 6);
        wall_counter = -1;
        spawnObjects();
        spawnObjects();
        spawnObjects();
        spawnObjects();
        spawnObjects();
    }

    void choose_sequence()
    {
        switch(sequence_index)
        {
            case 0:
                left_right();
                break;
            case 1:
                left_right_bothUp();
                break;
            case 2:
                Tpose_left_right();
                break;
            case 3:  
                up_squat();
                break;
            case 4:
                all_poses();
                break;
            case 5:
                random_pose();
                break;
            default:
                Debug.Log("Error : No such sequence yet : " + sequence_index);
                break;

        }
    }
    
    void left_right()
    {
        if (wall_index == 1)
        {
            wall_index = 2;
        }
        else
        {
            if (wall_index == 2)
            {
                wall_index = 1;
            }
            else
            {
                wall_index = 1;
            }
        }
    }

    void left_right_bothUp()
    {
        if (wall_index == 1 || wall_index==2 || wall_index ==3)
        {
            wall_index = (wall_index+1%3)+1;
        }
        else
        {
            wall_index = 1;
        }
    }

    void Tpose_left_right()
    {
        wall_index = ((wall_index + 1) % 3);
    }

    void all_poses()
    {
        wall_index = ((wall_index + 1) % 5);
    }
    void up_squat()
    {
        if (wall_index == 3)
        {
            wall_index = 4;
        }
        else
        {
            if (wall_index == 4)
            {
                wall_index = 3;
            }
            else
            {
                wall_index = 3;
            }
        }
    }

    void random_pose()
    {
        wall_index = Random.Range(0,5);
    }
}
