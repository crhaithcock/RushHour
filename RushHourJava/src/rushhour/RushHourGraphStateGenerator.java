package rushhour;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Stack;
import java.sql.*;
import java.text.SimpleDateFormat;
//import com.sun.javafx.css.Combinator;

//import rushhour.RushHour.PiecePlacement;


/***********************
 Reconceiving the design:
 	
 	command line input: num cars, num trucks
 	output: populate database table game_state with all states in the combinatorial class defined by num cars and num trucks
 	
 	
 	algorithm:
 	
 	If states for combinatorial class exist:
 		emit message
 		exit application
 	
 	recursively construct the game states for the given combinatorial class
 		if in base case (all pieces placed on the board):
 			add data to array structure
 			if length of data array > threshold (set threshold at 50k? )
 				bulk insert data into database
 				re initialize data array
 				
 				 	
**************************/

public class RushHourGraphStateGenerator {
	
	private FileWriter fw; // intermediate object only referenced to create buffered writer
	private BufferedWriter csvWriter;
	private Connection rushHourDbConnection;
	private Statement rushHourDbStatement;
	
	// see reference data at the bottom of this file
	private PiecePlacement[] piecePlacements;
	private PiecePlacement[] redCarPlacements = new PiecePlacement[5];

	private String boardArray[] = new String[36];
	public PiecePlacement redCarPlacement;
	private Stack<PiecePlacement> piecePlacementsInUse;
	
	private int numCars;
	private int numTrucks;
	
	private int gameNumber = 0;
	private int combinatorialClassId;
	
	// counters for tracking progress and flushing data on regular rhythm
	private long generatedStatesCounter = 0;
	
	private long dbBatchSizeLimit = 500000;
	private long dbCurBatchSize = 0;
	private long dbBatchCount = 0;
	private long dbTotalInsertsCount = 0;
	
	private long csvBatchSizeLimit = 5000;
	private long csvCurBatchSize;
	
	private Connection conn = null;
    private Statement insertStateStatement = null;
    
    private Calendar startDateTime, endDateTime, batchDateTime;
    private SimpleDateFormat formatDateAsTime = new SimpleDateFormat("YYY-MM-dd HH:mm:ss");

    
    static BigInteger Zero = new BigInteger("0");
    static BigInteger One = new BigInteger("1");
    
    
    public RushHourGraphStateGenerator(int numCars, int numTrucks){
    
    	this.numCars = numCars;
    	this.numTrucks = numTrucks;
    
    	initPiecePlacements();
    	//initDatabase();
    	csvOpen(); 
    	
    }
    


	
	private String csvFileName(){
		String filename,path;
		filename = "game_states_"; 
		filename += String.valueOf(numCars) + "_cars_";
		filename += String.valueOf(numTrucks) + "_trucks.csv";
		
		path = "C:/Users/cliff/workspace/Rush Hour With Java/data files/";
		
		return path + filename;
	}
	
	private boolean csvFileExists(){//int numCars, int numTrucks){
		File file = new File(csvFileName());
		return file.exists();	
	}
	
	
	private void csvClose(){
		if (csvWriter != null){
			try{
				csvWriter.close();
			}catch(IOException e){
				e.printStackTrace();
			}
		}
		if (fw != null){
			try{
				fw.close();
			} catch(IOException e){
				e.printStackTrace();
			}
		}
		
	}
	
	private void csvFlush(){
		try {
			csvWriter.flush();
		}catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	private boolean csvOpen(){

		File file;
		
		if (csvWriter != null){
			csvClose();
		}
				
		if (csvFileExists()){
			System.out.println("File Already Exists: " + csvFileName());
			System.exit(0);
			
		}
		
		file = new File(csvFileName());
		
		try{
			FileWriter fw = new FileWriter(file.getAbsoluteFile());
			csvWriter = new BufferedWriter(fw);
		}catch (IOException e) {
			e.printStackTrace();
		}
		
		csvWriteHeader();
		return true;
	}
	
	
	private void csvWriteHeader(){
		String header;
		header =  "game_number" +
				 ",comb_class_id" + 
				 ",game_hash_top" + 
				 ",game_hash_bottom" + 
				 ",is_goal_state" + 
				 ",optimal_neighbor" + 
				 ",red_car_end_a" + 
				 ",connected_component_id" +
				 ",topo_class_hash" + 
				 ",degree";
		try{
			csvWriter.write(header);
		}catch(IOException e){
			e.printStackTrace();
		}
	}
	

	private void csvWriterWriteNode(String game_number, String comb_class_id,String hash_top, String hash_bottom, String red_car_end_a, String topo_class_hash, String is_goal_state){
		String line;
		line =       game_number + 
			   "," + comb_class_id + 
			   "," + hash_top + 
			   "," + hash_bottom +
			   "," + is_goal_state + 
		       "," + 
			   "," + red_car_end_a + 
			   "," +
			   "," + topo_class_hash + 
			   ",";
		try{
			csvWriter.newLine();
			csvWriter.write(line);
		}catch(IOException e){
			e.printStackTrace();
		}
	}

	private void initDatabase(){
		rushHourDbConnection = null;
		rushHourDbStatement = null;
	    try {
	        Class.forName("org.sqlite.JDBC");
	        conn = DriverManager.getConnection("jdbc:sqlite:D:\\rush_hour.db");
	        conn.setAutoCommit(false);
	        //initPreparedStatement();
	        insertStateStatement = conn.createStatement();
	        
	    } catch ( Exception e ) {
	        System.err.println( e.getClass().getName() + ": " + e.getMessage() );
	        System.exit(0);
	      }
	        
	}
	
	private void initPreparedStatement(){
		try{
			String sql = "insert into game_state " + 
						 "( game_number,    comb_class_id,  game_hash_top,   game_hash_bottom," +
						 " is_goal_state,  red_car_end_a,  topo_class_hash, connected_component_id " + 
						 "values(?,?,?,?,?,?,?,?);";
			
			insertStateStatement = conn.prepareStatement(sql);
		} catch( Exception e){
			System.err.println(e.getClass().getName() + ": " + e.getMessage() );
	        System.exit(1);
		}
	}
	

	
	private void testSqlLiteJdbc(){
		Connection con = null;
		try {
		      Class.forName("org.sqlite.JDBC");
		      con = DriverManager.getConnection("jdbc:sqlite:C:/Users/cliff/workspace/rushHour/Data Model and SQL/Schema Definition and Bulk Load/rush_hour.db");
		    } catch ( Exception e ) {
		      System.err.println( e.getClass().getName() + ": " + e.getMessage() );
		      System.exit(0);
		    }
		    System.out.println("Opened database successfully");
	}


	private static Integer parseComLineNumCars(String [] args){
		int numCars = -1;
		
		try{
			numCars = Integer.parseInt(args[0]);
		}catch(Exception e){
			System.err.println( e.getClass().getName() + ": " + e.getMessage() );
			System.out.println("Unable to parse command line - number of cars: " + args[0]);
		    System.exit(1);
		}
		
		return numCars;
	}
	
	private static int parseComLineNumTrucks(String [] args){
		int numTrucks = -1;

		try{
			numTrucks = Integer.parseInt(args[1]);
		}catch(Exception e){
			System.err.println( e.getClass().getName() + ": " + e.getMessage() );
		    System.out.println("Unable to parse command line - number of trucks:" + args[1]);
			System.exit(1);
		}
		
		return numTrucks;
		
		
		
	}
	
	
	public static boolean validCommandLine(String [] args){
		
		int numCars, numTrucks;
		
		if (args == null){
			System.out.println("No Command Line Inputs. Expecting 2 Arguments.");
			return false;
		}
		
		if(args.length != 2){
			System.out.println("Wrong Number of Arguments. Expecting 2 Arguments.");
			return false;
		}
		
		numCars = parseComLineNumCars(args);
		numTrucks  = parseComLineNumTrucks(args);		
		
		if (numCars < 1 || numCars > 12){
			System.out.println("Number Of Cars Out Of Bounds. Must be between 1 and 12 inclusive");
			return false;
		}
		if (numTrucks < 0 || numTrucks > 4){
			System.out.println("Number Of Trucks Out Of Bounds. Must be between 0 and 4 inclusive");
			return false;
		}	
		
		return true;
	}

	
	private boolean nodesAlreadyInDb(){//int numCars, int numTrucks){
		
		int combClassId = (int) (Math.pow(2,numCars) * Math.pow(3,numTrucks));
		int classCount;
		boolean dataExists = false;
		ResultSet rs;
		String sql;
		Statement stmt = null;
		
		sql = "Select count(*) as cnt from game_state where comb_class_id = " + combClassId + ";";
		
		try{	
			stmt = conn.createStatement();
			rs = stmt.executeQuery(sql);
			
			rs.next();
			classCount = rs.getInt("cnt");
			if (classCount > 0){
				dataExists = true;
			}		
			else{
				dataExists =  false;		
			}
		
		
		}catch(Exception e){
			System.err.println( e.getClass().getName() + ": " + e.getMessage() );
		    System.exit(1);
		}

		return dataExists;
	}
	
	public void validateCommandLine(){
		
		// if there is an issue exit program. This allows static main to call non-static methods
		
	}
	
	
	
	public static void main(String args[]){
		int numCars, numTrucks;		
		//RushHourGraphStateGenerator stateCalculator = new RushHourGraphStateGenerator();
		RushHourGraphStateGenerator stateCalculator;
		
		// initialize these to make IDE complaints go away. But inin to out of bound values.
		numCars = -1;
		numTrucks = -1;
		
		if (args == null){
			System.out.println("No Command Line Inputs. Expecting 2 Arguments.");
			System.exit(1);
		}
		
		if(args.length != 2){
			System.out.println("Wrong Number of Arguments. Expecting 2 Arguments.");
			System.exit(1);
		}
		
		numCars = parseComLineNumCars(args);
		numTrucks = parseComLineNumTrucks(args);
		
		if (numCars < 1 || numCars > 12){
			System.out.println("Number Of Cars Out Of Bounds. Must be between 1 and 12 inclusive");
			System.exit(1);
		}
		if (numTrucks < 0 || numTrucks > 4){
			System.out.println("Number Of Trucks Out Of Bounds. Must be between 0 and 4 inclusive");
			System.exit(1);
		}	
		
		stateCalculator = new RushHourGraphStateGenerator(numCars,numTrucks);
		
		
		// validate result not already produced
//		if ( stateCalculator.nodesAlreadyInCsv()){
//			System.out.println("Already Generated Data For Given Inputs.");
//			System.exit(1);
//		}
		
		stateCalculator.generateStates();
		
		System.out.println("Done Building States.");
		// TODO!!! Write Summary Stats upon completion: time to complete, num states written, etc.
		
	} // end main
	
	// At the time of this writing, my computer rebooted with only 76.2mm states for comb class: 9 cars, 3 trucks.
	// I was looking for a way to jump start the state generator at 76.2mmm + 1 state.
	// I quickly ran into the computational problem
	private void generateStatesMidRecursion(int combClassId){
		
		String sql;
		// get max state data from db
		sql = "select game_number, game_hash_top, game_hash_bottom, red_car_end_a \n" + 
		      "from game_state \n" +
			  "where comb_class_id = " + combClassId + "\n" +
			  "      and game_number = (select max(game_number) \n" +
		      "                         from game_state where comb_class_id = " + combClassId;
		
		// reconstitute program state to jump into recursion.
		
		
		
	}
	
	
	private void generateStates(){
		
		combinatorialClassId = (int) (Math.pow(2,numCars) * Math.pow(3,numTrucks));
		
		startDateTime = Calendar.getInstance();
		
		//initCsvWriter(numCars, numTrucks)

		// if states exist, pick up where states left off
		// if no states exists, start from scratch
		
		// sql to get last state inserted for the combinatorial class
		// convert the board hashes into piece placements
		// put each piece placement on the board (except red car)
		// determine list of remaining redCarPiecePlacements
		// for each red car piece placement:
		// 		place the red car
		//      make the recursive call
		
		// create a separate routine to init data when generating states halted before completing comb class id
		
		
		for(PiecePlacement p:redCarPlacements){
			
			redCarPlacement = p;
			placePieceOnBoard(p);
			
			generateStatesRecursively(numCars - 1, numTrucks,0);
			
			removePieceFromBoard(p);
		}
	
		
		
		//commit last round of updates to prepared statement; open ended batch
		if (	dbCurBatchSize > 0){
			try{
				insertStateStatement.executeBatch();
			}
			catch (Exception e){
				System.err.println( e.getClass().getName() + ": " + e.getMessage() );
			    System.out.println("Unable to Save Partial Batch Of Final Inserts");
				System.exit(1);
			}
		}
		
		
		//closeDatabase();
		
		csvClose();
		
		endDateTime = Calendar.getInstance();
		
		System.out.println ("Start Time: " + formatDateAsTime.format( startDateTime.getTime() ) );
		System.out.println("End Time: " + formatDateAsTime.format( endDateTime.getTime() ) );
		System.out.println("Total States Generated: " + generatedStatesCounter);
		
		// print summary data
		
		
		
	}


	private void close(){
		closeDatabase();
	}
	
	private void closeDatabase(){
		try {
				conn.commit();
				insertStateStatement.close();
				conn.close();
		     
			} catch ( Exception e ) {
		      System.err.println( e.getClass().getName() + ": " + e.getMessage() );
		      System.exit(1);
		    }		
		
		
		
	}
	
	
	private void recordState(){
		recordStateCsv();
		//recordStateDb();
		
	}
	private void recordStateDb(){
		//System.out.println("Entering recordStateDb; dbCurbBatchSize:" + dbCurBatchSize);
		String sql;		
		String gameNum = String.valueOf(gameNumber);
		String combClassId = String.valueOf(combinatorialClassId);
		String boardHashTop = String.valueOf(boardHashTop());
		String boardHashBottom = String.valueOf(boardHashBottom());
		String redCarEndA = String.valueOf(redCarPlacement.end_a);
		String topoClassHash = String.valueOf(topoHash());
		String isGoalState;
		if (isGoalState()){
			isGoalState = "1";
		}
		else{
			isGoalState = "0";
		}
		
		dbCurBatchSize += 1;// dbCurBatchSize.add(One);
		
		dbTotalInsertsCount += 1;// = dbTotalInsertsCount.add(One);
		 
		sql = "insert into game_state " + 
				 "( game_number,    comb_class_id,  game_hash_top,   game_hash_bottom," +
				 " is_goal_state,  red_car_end_a,  topo_class_hash) values("  +
				 gameNum + "," +
				 combClassId + "," +
				 boardHashTop + "," +
				 boardHashBottom + "," +
				 isGoalState + "," +
				 redCarEndA + "," + 
				 topoClassHash + ");";
		
		try{
			insertStateStatement.addBatch(sql);
			//System.out.println("Recording Batch with size:" + dbCurBatchSize );
		}catch(Exception e){
			System.err.println( e.getClass().getName() + ": " + e.getMessage() );
		    System.out.println("Error Adding SQL to Batch.");
		    System.out.println("insert count:" + String.valueOf(dbTotalInsertsCount));
		    
		    System.exit(1);	     
		}
		
		if( dbCurBatchSize == dbBatchSizeLimit){
			dbBatchCount +=1; // dbBatchCount.add(One);
			dbCurBatchSize = 0;// = Zero;
			try{
				insertStateStatement.executeBatch();
				conn.commit();
			    //# System.out.println( sdf.format(cal.getTime()) );
				batchDateTime = Calendar.getInstance();
				System.out.println ("Committed batch.Total Inserts: " + dbTotalInsertsCount + " ; Cur Time: " + formatDateAsTime.format( batchDateTime.getTime() ) );
				
	
			}catch(Exception e){
				System.err.println( e.getClass().getName() + ": " + e.getMessage() );
			    System.out.println("Error Executing SQL Batch Insert.");
			    System.out.println("final insert count with this batch:" + String.valueOf(dbTotalInsertsCount));
			    System.exit(1);	     
			}
		}
		
		
		/*
		 * if batch size limit reached
		 * 		execute prepared statement
		 * 		set prepared statement to new instance
		 * 		
		 **/
		
	}
	
	private void recordStateCsv(){
		
		String gameNum = String.valueOf(gameNumber);
		String combClassId = String.valueOf(combinatorialClassId);
		String boardHashTop = String.valueOf(boardHashTop());
		String boardHashBottom = String.valueOf(boardHashBottom());
		String redCarEndA = String.valueOf(redCarPlacement.end_a);
		String topoClassHash = String.valueOf(topoHash());
		String isGoalState = String.valueOf(isGoalState());
	
		
		csvWriterWriteNode(gameNum,combClassId,boardHashTop, boardHashBottom, redCarEndA,topoClassHash,isGoalState);
		
		generatedStatesCounter += 1;
		csvCurBatchSize += 1;
		if (csvCurBatchSize == csvBatchSizeLimit){
			csvFlush();
			System.out.println("States Generated: " + generatedStatesCounter + " :" + formatDateAsTime.format( Calendar.getInstance().getTime() ) );
			csvCurBatchSize = 0;
		}
		
		
	}

	
//	header =  "game_number" +
//			 ",comb_class_id" + 
//			 ",game_hash_top" + 
//			 ",game_hash_bottom" + 
//			 ",is_goal_state" + 
//			 ",optimal_neighbor" + 
//			 ",red_car_end_a" + 
//			 ",connected_component_id" +
//			 ",topo_class_hash" + 
//			 ",degree";
	
	private void databaseWriteNode(String game_number, String comb_class_id,String hash_top, String hash_bottom, String red_car_end_a, String topo_class_hash, String is_goal_state){
		String sql;
		String is_goal_state_for_sqlite;
		
		if (is_goal_state == "false"){
			is_goal_state_for_sqlite = "0";
		}
		else{
			is_goal_state_for_sqlite = "1";
		}
		
		sql = "insert into game_state (game_number, comb_class_id,game_hash_top, game_hash_bottom, is_goal_state,red_car_end_a,topo_class_hash) values ";
		sql = sql + "(" +  game_number + 
					"," + comb_class_id + 
					"," + hash_top + 
					"," + hash_bottom +
					"," + is_goal_state_for_sqlite + 
					"," + red_car_end_a + 
					"," + topo_class_hash + 
					")";
		try{
			//rushHourDbStatement = rushHourDbConnection.createStatement();
			rushHourDbStatement.executeUpdate(sql);
			//rushHourDbConnection.commit();
			rushHourDbStatement.close();
			
		}catch(Exception e){
			System.err.println( e.getClass().getName() + ": " + e.getMessage() );
		    System.exit(0);
		}
	}

	
	
	// the recursion requires knowing where on the board to start attempting to place pieces.
	private void generateStatesRecursively (int numCars, int numTrucks, int curPosition){
		
		// System.out.println("Entering Recursive Call. Cars = " + numCars + ", Trucks = " + numTrucks);
		// we can improve this bailout rather cheaply 
		//     	* count of open space in board[curPosition:] is less than numCars + numTrucks
		//		* 
		
		
		if(numCars == 0 && numTrucks == 0){
			//System.out.println("In bottom Case");
			gameNumber += 1;
			recordState();
			return;
		}
		
		// We have reached the end of the board without any way to add the additional pieces.
		// 35 => 6x6 board
		if (curPosition == 35){
			return;
		}
		
		
		// !!!! TODO - consider tighter constraints on the bailout condition.
		
		if (numCars > 0){
			for (int i = curPosition; i < 36; i++){
				for (PiecePlacement p: this.groupedCarPlacements.get(i)){
					if (boardArray[p.end_a] == this.BLANK_SPACE && boardArray[p.end_b] == this.BLANK_SPACE){
						placePieceOnBoard(p);
						generateStatesRecursively(numCars-1, numTrucks, i +1);
						removePieceFromBoard(p);
					}
				}
			}
		}
		
		if (numTrucks > 0){
			for (int i = curPosition; i < 36 ; i++){
				for (PiecePlacement p: this.groupedTruckPlacements.get(i)){
					if (this.boardArray[p.end_a] == this.BLANK_SPACE && this.boardArray[p.end_b] == this.BLANK_SPACE){
						if( (p.orientation == "Vertical" && this.boardArray[p.end_a + 6] == this.BLANK_SPACE) ||
							(p.orientation == "Horizontal" && this.boardArray[p.end_a + 1] == this.BLANK_SPACE)){
							placePieceOnBoard(p);
							generateStatesRecursively(numCars, numTrucks - 1, i + 1);
							removePieceFromBoard(p);
						}
					}
				}
			}
		}
		
	}
	private void placePieceOnBoard(PiecePlacement p){
		
		piecePlacementsInUse.push(p);
		
		if (p.length == 2){
			if (p.orientation == "Vertical"){
				boardArray[p.end_a] = VERTICAL_CAR;
				boardArray[p.end_b] = VERTICAL_CAR;
			}
			else{
				boardArray[p.end_a] = HORIZONTAL_CAR;
				boardArray[p.end_b] = HORIZONTAL_CAR;
			}
		}
		else{
			if (p.orientation == "Vertical"){
				boardArray[p.end_a]	 	= VERTICAL_TRUCK;
				boardArray[p.end_a + 6] = VERTICAL_TRUCK;
				boardArray[p.end_b] 	= VERTICAL_TRUCK;
			}
			else{
				boardArray[p.end_a]	 	= HORIZONTAL_TRUCK;
				boardArray[p.end_a + 1] = HORIZONTAL_TRUCK;
				boardArray[p.end_b] 	= HORIZONTAL_TRUCK;
			}
		}
	}

	
	public void removePieceFromBoard(PiecePlacement p){
		
		piecePlacementsInUse.pop();
		
		if (p.length == 2){
			if (p.orientation == "Vertical"){
				boardArray[p.end_a] = BLANK_SPACE;
				boardArray[p.end_b] = BLANK_SPACE;
			}
			else{
				boardArray[p.end_a] = BLANK_SPACE;
				boardArray[p.end_b] = BLANK_SPACE;
			}
		}
		else{
			if (p.orientation == "Vertical"){
				boardArray[p.end_a]	 	= BLANK_SPACE;
				boardArray[p.end_a + 6] = BLANK_SPACE;
				boardArray[p.end_b] 	= BLANK_SPACE;
			}
			else{
				boardArray[p.end_a]	 	= BLANK_SPACE;
				boardArray[p.end_a + 1] = BLANK_SPACE;
				boardArray[p.end_b] 	= BLANK_SPACE;
			}
		}		
	}
	
	
	
	/***************************************
	 	Board IO Utilities
	***************************************/
	private boolean isGoalState(){
		return ( redCarPlacement.end_b == 17);
	}
	
	
	private long boardHashTop(){
		
		String top18spaces = boardArray[0]  + boardArray[1]  + boardArray[2]  + boardArray[3]  + boardArray[4]  +
					         boardArray[5]  + boardArray[6]  + boardArray[7]  + boardArray[8]  + boardArray[9]  +
					         boardArray[10] + boardArray[11] + boardArray[12] + boardArray[13] + boardArray[14] +
					         boardArray[15] + boardArray[16] + boardArray[17];
		
					         
		// build string of the top 18 board spaces
		return Long.parseLong(top18spaces, 2);
		
	}
	
	
	private long boardHashBottom(){
		
		String bottom18Spaces =  boardArray[18] + boardArray[19] + boardArray[20] + boardArray[21] + boardArray[22] +
						         boardArray[23] + boardArray[24] + boardArray[25] + boardArray[26] + boardArray[27] +
						         boardArray[28] + boardArray[29] + boardArray[30] + boardArray[31] + boardArray[32] +
						         boardArray[33] + boardArray[34] + boardArray[35];
		
		// build string of the bottom 18 board spaces
		return Long.parseLong(bottom18Spaces, 2);
	}


	// Create a hash that represents the topological class for the game state implied by 
	// the shared data structures representing the RH Board.
	// The hash is built by converting a bit string into a long.
	// The hash bit string is a concatenation of a bit string representation for each row and column.
	// The bit string representation for each row/col is defined by the number of cars/trucks within that row/col
	private long topoHash(){
		
		String hashBitString;
		
		/* row1 row2 row3 ... row6 col1 col2 ... col6 */
		int[] topo_row_car_count 	= new int[6];
		int[] topo_row_truck_count 	= new int[6];
		int[] topo_col_car_count 	= new int[6];
		int[] topo_col_truck_count 	= new int[6];
		String[] topo_rows = new String[6];
		String[] topo_cols = new String[6];
		
		// Get the count of cars/truck for each row/col of the board
		for(PiecePlacement p: piecePlacementsInUse){
			if (p.orientation == "Vertical"   && p.length == 2){topo_col_car_count[p.end_a % 6] += 1;}
			if (p.orientation == "Vertical"   && p.length == 3){topo_col_truck_count[p.end_a % 6] += 1;}
			if (p.orientation == "Horizontal" && p.length == 2){topo_row_car_count[p.end_a / 6] += 1;}
			if (p.orientation == "Horizontal" && p.length == 3){topo_row_truck_count[p.end_a / 6] +=1;}
		}
     
		// for each row/col, what is the bit string for that row/col?
		for (int i =0; i<6; i++){
			topo_rows[i] = topoSingleRowColHash(topo_row_car_count[i],topo_row_truck_count[i]);
			topo_cols[i] = topoSingleRowColHash(topo_col_car_count[i],topo_col_truck_count[i]);
		}	
		
		// Now glue together all of the individual row and col bit strings into a single bit string
		hashBitString = topo_rows[0] + topo_rows[1] + topo_rows[2] + topo_rows[3] + topo_rows[4] + topo_rows[5] +
				        topo_cols[0] + topo_cols[1] + topo_cols[2] + topo_cols[3] + topo_cols[4] + topo_cols[5];
	
		return Long.parseLong(hashBitString, 2); // convert hash string to long using base 2 numbers
	
	}
	
	
	private String topoSingleRowColHash(int car_count, int truck_count){
		
		if (car_count == 0 && truck_count == 0 ){return TOPO_EMPTY;}
		if (car_count == 0 && truck_count == 1 ){return TOPO_ONE_TRUCK;}
		if (car_count == 0 && truck_count == 2 ){return TOPO_TWO_TRUCKS;}
		
		if (car_count == 1 && truck_count == 0 ){return TOPO_ONE_CAR;}
		if (car_count == 1 && truck_count == 1 ){return TOPO_ONE_CAR_ONE_TRUCK;}
		
		if (car_count == 2 && truck_count == 0 ){return TOPO_TWO_CARS;}
		
		if (car_count == 3 && truck_count == 0 ){return TOPO_THREE_CARS;}
		
		return ""; // return statement to make Compiler happy
	}
	/****************************************
	 			
	 			Reference Data 
	 			
	****************************************/
	private String BLANK_SPACE 		= "000";
	private String VERTICAL_CAR 	= "001";
	private String VERTICAL_TRUCK 	= "010";
	private String HORIZONTAL_CAR 	= "011";
	private String HORIZONTAL_TRUCK = "100";
	
	private String TOPO_EMPTY              = "000";
	private String TOPO_ONE_CAR            = "001";
	private String TOPO_TWO_CARS           = "010";
	private String TOPO_THREE_CARS         = "011";
	private String TOPO_ONE_TRUCK          = "100";
	private String TOPO_TWO_TRUCKS         = "101";
	private String TOPO_ONE_CAR_ONE_TRUCK  = "110";
	
	
	private class PiecePlacement{
		public int end_a;
		public int end_b;
		public String orientation;
		public int length;
		
		@Override
		public String toString(){
			return "end_a: " + this.end_a + "; end_b: " + this.end_b + "; length: " + this.length + "; orientation: " + this.orientation;
		}
	}
	
	private ArrayList<ArrayList<PiecePlacement>> groupedCarPlacements;
	private ArrayList<ArrayList<PiecePlacement>> groupedTruckPlacements;
	
	
	private void initPiecePlacements(){
		piecePlacements = new PiecePlacement[108];
		groupedCarPlacements = new ArrayList<ArrayList<PiecePlacement>>();
		groupedTruckPlacements = new ArrayList<ArrayList<PiecePlacement>>();
		piecePlacementsInUse = new Stack<PiecePlacement>();
		
		for(int i=0;i<108;i++){
			piecePlacements[i] = new PiecePlacement();
		}
		
		for(int i = 0; i< 36; i++){
			boardArray[i] = BLANK_SPACE;
		}
		
		for(int i=0; i<36; i++){
			ArrayList<PiecePlacement> carList = new ArrayList<PiecePlacement>();
			ArrayList<PiecePlacement> truckList = new ArrayList<PiecePlacement>();
			
			groupedCarPlacements.add(carList);
			groupedTruckPlacements.add(truckList);
		}
		
		int index = 0;
		
		//horizontal cars
		for (int i = 0; i<6; i++){
			for(int j = 0; j<5 ;j++){
				PiecePlacement x = piecePlacements[index];
				x.end_a = 6*i+j;
				x.end_b = 6*i+j+1;
				x.length = 2;
				x.orientation = "Horizontal";
				index +=1;
				groupedCarPlacements.get(x.end_a).add(x);
			}
		}
		
		//vertical cars
		for (int i=0; i<5; i++){
			for(int j=0; j<6;j++){
				PiecePlacement x = piecePlacements[index];
				x.end_a = 6*i+j;
				x.end_b = 6*i+j+6;
				x.length = 2;
				x.orientation = "Vertical";
				index ++;
				groupedCarPlacements.get(x.end_a).add(x);
			}
		}
		
		//horizontal trucks
		for(int i=0; i<6; i++){
			for(int j=0; j<4; j++){
				PiecePlacement x = this.piecePlacements[index];
				x.end_a = 6*i+j;
				x.end_b = 6*i+j+2;
				x.length = 3;
				x.orientation = "Horizontal";
				index++;
				groupedTruckPlacements.get(x.end_a).add(x);
			}
		}
		
		//vertical trucks
		for(int i=0;i<4;i++){
			for(int j=0;j<6;j++){
				PiecePlacement x = piecePlacements[index];
				x.end_a = 6*i+j;
				x.end_b = 6*i+j+12;
				x.length = 3;
				x.orientation = "Vertical";
				index++;
				groupedTruckPlacements.get(x.end_a).add(x);
			}
		}
		
		//red car placements
		int redCarIndex = 0;
		for(PiecePlacement i:piecePlacements){
			if(i.end_a > 11 && i.end_a<18 && i.length == 2 && i.orientation == "Horizontal"){
				redCarPlacements[redCarIndex] = i;
				redCarIndex++;
			}
		
		}
	}
	
	
	
	
	
}

