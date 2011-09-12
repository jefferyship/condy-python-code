package ecc.warning.pojo;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Name;
import org.nutz.dao.entity.annotation.Table;

@Table("MONITOR_ZX_ALARM_CONFIG")
public class ZxAlarmConfig {
	@Column("ALARM_NAME")
	private String alarmName;
	@Name
	@Column("ALARM_TYPE_ID")
	private String alarmTypeId;
	@Column("ALARM_LEVEL")
	private String alarmLevel;
	/**
	 * @return the alarmName
	 */
	public String getAlarmName() {
		return alarmName;
	}
	/**
	 * @param alarmName the alarmName to set
	 */
	public void setAlarmName(String alarmName) {
		this.alarmName = alarmName;
	}
	/**
	 * @return the alarmTypeId
	 */
	public String getAlarmTypeId() {
		return alarmTypeId;
	}
	/**
	 * @param alarmTypeId the alarmTypeId to set
	 */
	public void setAlarmTypeId(String alarmTypeId) {
		this.alarmTypeId = alarmTypeId;
	}
	/**
	 * @return the alarmLevel
	 */
	public String getAlarmLevel() {
		return alarmLevel;
	}
	/**
	 * @param alarmLevel the alarmLevel to set
	 */
	public void setAlarmLevel(String alarmLevel) {
		this.alarmLevel = alarmLevel;
	}
	

}
