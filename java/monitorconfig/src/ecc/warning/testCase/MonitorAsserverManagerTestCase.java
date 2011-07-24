package ecc.warning.testCase;

import java.util.List;

import ecc.warning.manager.MonitorAsserverManager;
import ecc.warning.pojo.MonitorAsserver;
import junit.framework.TestCase;

public class MonitorAsserverManagerTestCase extends TestCase {

	private MonitorAsserverManager mam;
	protected void setUp() throws Exception {
		super.setUp();
		mam=new MonitorAsserverManager();
	}
	
	public void testList(){
		List<MonitorAsserver> list=mam.list(null,null);
		assertNotNull(list);
		assertFalse(list.size()==0);
		System.out.println("aaaa:"+list.get(0).getMonitorName());
	}
	public void testQuery(){
		List<MonitorAsserver> list=mam.list("monitorName", "¶Ë¿Ú1");
		assertNotNull(list);
		assertFalse(list.size()==0);
	}
	
	public void testInsert(){
		MonitorAsserver ma=new MonitorAsserver();
		ma.setAboutSystem("Condy");
		ma.setSts("A");
		ma.setMonitorName("Condy_test");
		ma.setUrl("http://134.128.51.131:9082/iserv/iserv/CallUrcp.jsp");
		ma.setUrlContent("name=getRouteInfo&param=88203511100000591101001");
		assertTrue(mam.insert(ma));
		assertNotNull(ma.getSeq());
	}
	
	public void testUpdate(){
		MonitorAsserver ma=mam.getBySeq("4");
		ma.setSts("B");
		assertTrue(mam.update(ma));
	}
	
	public void testDelete(){
		MonitorAsserver ma=mam.getBySeq("4");
		assertTrue(mam.delete(ma.getSeq()));
	}

	protected void tearDown() throws Exception {
		super.tearDown();
	}

}
