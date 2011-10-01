package ecc.warning.testCase;

import java.sql.Timestamp;
import java.util.Date;
import java.util.List;

import org.nutz.json.Json;

import ecc.warning.manager.ZxWarnManager;
import ecc.warning.pojo.ZxAlarmLog;
import junit.framework.TestCase;

public class ZxWarnManagerTestCase extends TestCase {

	private ZxWarnManager zxWarnManager;
	protected void setUp() throws Exception {
		super.setUp();
		zxWarnManager=new ZxWarnManager();
	}
	
	public void testGetZxAlarmLog(){
		Timestamp startDate=new Timestamp(new Date().getTime()-24*60*60*1000);
		Timestamp endDate=null;
		String alarmLevel="4";
		String alarmTypeId="almpcm";
		int totalCount=zxWarnManager.getZxAlarmLogOfCount("2011-09-01", null, alarmLevel, alarmTypeId);
		List<ZxAlarmLog> list=zxWarnManager.getZxAlarmLog("2011-09-01", null, alarmLevel, alarmTypeId, 0, 10,totalCount);
		assertFalse(list.size()==0);
		System.out.println(Json.toJson(list));
		System.out.println("aaaaaaaaaaa:"+totalCount);
	}

}
