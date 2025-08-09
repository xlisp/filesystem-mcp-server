## pip install astropy pytz mcp
from typing import Any, List, Dict
import math
from datetime import datetime, timezone
import pytz
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, get_sun, get_moon, get_body
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("astronomy")

# 行星列表
PLANETS = ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

# 亮星和星云数据 (简化版本)
BRIGHT_STARS = {
    'sirius': {'ra': 101.287, 'dec': -16.716, 'mag': -1.46, 'name': '天狼星'},
    'canopus': {'ra': 95.988, 'dec': -52.696, 'mag': -0.74, 'name': '老人星'},
    'arcturus': {'ra': 213.915, 'dec': 19.182, 'mag': -0.05, 'name': '大角星'},
    'vega': {'ra': 279.234, 'dec': 38.784, 'mag': 0.03, 'name': '织女星'},
    'capella': {'ra': 79.172, 'dec': 45.998, 'mag': 0.08, 'name': '五车二'},
    'rigel': {'ra': 78.634, 'dec': -8.202, 'mag': 0.13, 'name': '参宿七'},
    'procyon': {'ra': 114.825, 'dec': 5.225, 'mag': 0.34, 'name': '南河三'},
    'betelgeuse': {'ra': 88.793, 'dec': 7.407, 'mag': 0.50, 'name': '参宿四'},
    'altair': {'ra': 297.696, 'dec': 8.868, 'mag': 0.77, 'name': '牛郎星'},
    'spica': {'ra': 201.298, 'dec': -11.161, 'mag': 0.97, 'name': '角宿一'}
}

MESSIER_OBJECTS = {
    'M1': {'ra': 83.633, 'dec': 22.015, 'type': 'supernova remnant', 'name': '蟹状星云'},
    'M31': {'ra': 10.685, 'dec': 41.269, 'type': 'galaxy', 'name': '仙女座星系'},
    'M42': {'ra': 83.822, 'dec': -5.391, 'type': 'nebula', 'name': '猎户座星云'},
    'M45': {'ra': 56.75, 'dec': 24.117, 'type': 'open cluster', 'name': '昴宿星团'},
    'M51': {'ra': 202.47, 'dec': 47.195, 'type': 'galaxy', 'name': '漩涡星系'},
    'M57': {'ra': 283.396, 'dec': 33.029, 'type': 'planetary nebula', 'name': '环状星云'},
    'M81': {'ra': 148.89, 'dec': 69.065, 'type': 'galaxy', 'name': '波德星系'},
    'M101': {'ra': 210.80, 'dec': 54.349, 'type': 'galaxy', 'name': '风车星系'},
    'M13': {'ra': 250.42, 'dec': 36.460, 'type': 'globular cluster', 'name': '武仙座球状星团'},
    'M20': {'ra': 270.92, 'dec': -23.033, 'type': 'nebula', 'name': '三裂星云'}
}

def get_observation_time(time_str: str = None, timezone_str: str = "UTC") -> Time:
    """获取观测时间"""
    if time_str:
        try:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        except:
            dt = datetime.now(timezone.utc)
    else:
        dt = datetime.now(timezone.utc)
    
    if timezone_str != "UTC":
        try:
            tz = pytz.timezone(timezone_str)
            dt = tz.localize(dt.replace(tzinfo=None)) if dt.tzinfo is None else dt.astimezone(tz)
        except:
            pass
    
    return Time(dt)

def get_location(latitude: float, longitude: float, elevation: float = 0) -> EarthLocation:
    """获取观测地点"""
    return EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg, height=elevation*u.m)

def format_coordinates(alt: float, az: float) -> str:
    """格式化坐标"""
    return f"高度角: {alt:.1f}°, 方位角: {az:.1f}°"

def is_visible(altitude: float, min_altitude: float = 10.0) -> bool:
    """判断天体是否可见"""
    return altitude > min_altitude

@mcp.tool()
async def get_planets_visibility(latitude: float, longitude: float, time_str: str = None, 
                               timezone_str: str = "UTC", min_altitude: float = 10.0) -> str:
    """获取当前可见的行星信息
    
    Args:
        latitude: 纬度 (-90 to 90)
        longitude: 经度 (-180 to 180)
        time_str: 时间 (ISO格式，如 "2024-01-01T20:00:00", 默认为当前时间)
        timezone_str: 时区 (如 "Asia/Shanghai", 默认为 "UTC")
        min_altitude: 最小可见高度角 (度, 默认10度)
    """
    try:
        time = get_observation_time(time_str, timezone_str)
        location = get_location(latitude, longitude)
        frame = AltAz(obstime=time, location=location)
        
        visible_planets = []
        all_planets_info = []
        
        for planet in PLANETS:
            try:
                body = get_body(planet, time)
                altaz = body.transform_to(frame)
                
                alt = altaz.alt.degree
                az = altaz.az.degree
                
                planet_info = f"{planet.upper()}: {format_coordinates(alt, az)}"
                all_planets_info.append(planet_info)
                
                if is_visible(alt, min_altitude):
                    visible_planets.append(f"✓ {planet_info}")
                    
            except Exception as e:
                all_planets_info.append(f"{planet.upper()}: 计算错误 - {str(e)}")
        
        result = f"观测时间: {time.iso}\n"
        result += f"观测地点: {latitude:.2f}°, {longitude:.2f}°\n"
        result += f"最小可见高度角: {min_altitude}°\n\n"
        
        if visible_planets:
            result += "当前可见的行星:\n" + "\n".join(visible_planets)
        else:
            result += "当前没有行星在可见范围内"
            
        result += "\n\n所有行星位置:\n" + "\n".join(all_planets_info)
        
        return result
        
    except Exception as e:
        return f"计算行星可见性时发生错误: {str(e)}"

@mcp.tool()
async def get_planet_altitude(planet_name: str, latitude: float, longitude: float, 
                            time_str: str = None, timezone_str: str = "UTC") -> str:
    """获取特定行星的高度角和方位角
    
    Args:
        planet_name: 行星名称 (mercury, venus, mars, jupiter, saturn, uranus, neptune)
        latitude: 纬度 (-90 to 90)
        longitude: 经度 (-180 to 180)
        time_str: 时间 (ISO格式，如 "2024-01-01T20:00:00", 默认为当前时间)
        timezone_str: 时区 (如 "Asia/Shanghai", 默认为 "UTC")
    """
    try:
        planet_name = planet_name.lower()
        if planet_name not in PLANETS:
            return f"不支持的行星名称。支持的行星: {', '.join(PLANETS)}"
            
        time = get_observation_time(time_str, timezone_str)
        location = get_location(latitude, longitude)
        frame = AltAz(obstime=time, location=location)
        
        body = get_body(planet_name, time)
        altaz = body.transform_to(frame)
        
        alt = altaz.alt.degree
        az = altaz.az.degree
        
        visibility_status = "可见" if is_visible(alt) else "不可见"
        
        result = f"{planet_name.upper()} 位置信息:\n"
        result += f"观测时间: {time.iso}\n"
        result += f"观测地点: {latitude:.2f}°, {longitude:.2f}°\n"
        result += f"{format_coordinates(alt, az)}\n"
        result += f"可见性: {visibility_status}"
        
        if alt < 0:
            result += " (在地平线以下)"
        elif alt < 10:
            result += " (接近地平线，可能受大气影响)"
            
        return result
        
    except Exception as e:
        return f"获取{planet_name}位置时发生错误: {str(e)}"

@mcp.tool()
async def get_moon_info(latitude: float, longitude: float, time_str: str = None, 
                       timezone_str: str = "UTC") -> str:
    """获取月亮的详细信息
    
    Args:
        latitude: 纬度 (-90 to 90)
        longitude: 经度 (-180 to 180)
        time_str: 时间 (ISO格式，如 "2024-01-01T20:00:00", 默认为当前时间)
        timezone_str: 时区 (如 "Asia/Shanghai", 默认为 "UTC")
    """
    try:
        time = get_observation_time(time_str, timezone_str)
        location = get_location(latitude, longitude)
        frame = AltAz(obstime=time, location=location)
        
        moon = get_moon(time)
        moon_altaz = moon.transform_to(frame)
        
        alt = moon_altaz.alt.degree
        az = moon_altaz.az.degree
        
        # 计算月相 (简化计算)
        sun = get_sun(time)
        
        # 月亮和太阳的角度差
        separation = moon.separation(sun).degree
        
        if separation < 45:
            phase = "新月"
        elif separation < 90:
            phase = "峨眉月"
        elif separation < 135:
            phase = "上弦月"
        elif separation < 180:
            phase = "盈凸月"
        elif separation < 225:
            phase = "满月"
        elif separation < 270:
            phase = "亏凸月"
        elif separation < 315:
            phase = "下弦月"
        else:
            phase = "残月"
        
        visibility_status = "可见" if is_visible(alt) else "不可见"
        
        result = f"月亮信息:\n"
        result += f"观测时间: {time.iso}\n"
        result += f"观测地点: {latitude:.2f}°, {longitude:.2f}°\n"
        result += f"{format_coordinates(alt, az)}\n"
        result += f"月相: {phase}\n"
        result += f"与太阳角距: {separation:.1f}°\n"
        result += f"可见性: {visibility_status}"
        
        if alt < 0:
            result += " (在地平线以下)"
        elif alt < 10:
            result += " (接近地平线)"
            
        return result
        
    except Exception as e:
        return f"获取月亮信息时发生错误: {str(e)}"

@mcp.tool()
async def get_deep_sky_objects(latitude: float, longitude: float, time_str: str = None,
                             timezone_str: str = "UTC", min_altitude: float = 30.0,
                             object_type: str = "all") -> str:
    """获取当前可见的深空天体 (星云、星团、星系等)
    
    Args:
        latitude: 纬度 (-90 to 90)
        longitude: 经度 (-180 to 180)
        time_str: 时间 (ISO格式，如 "2024-01-01T20:00:00", 默认为当前时间)
        timezone_str: 时区 (如 "Asia/Shanghai", 默认为 "UTC")
        min_altitude: 最小可见高度角 (度, 默认30度)
        object_type: 天体类型筛选 ("all", "nebula", "galaxy", "cluster")
    """
    try:
        time = get_observation_time(time_str, timezone_str)
        location = get_location(latitude, longitude)
        frame = AltAz(obstime=time, location=location)
        
        visible_objects = []
        all_objects_info = []
        
        for obj_id, obj_data in MESSIER_OBJECTS.items():
            # 类型筛选
            if object_type != "all":
                if object_type == "nebula" and "nebula" not in obj_data['type']:
                    continue
                elif object_type == "galaxy" and "galaxy" not in obj_data['type']:
                    continue
                elif object_type == "cluster" and "cluster" not in obj_data['type']:
                    continue
            
            try:
                coord = SkyCoord(ra=obj_data['ra']*u.deg, dec=obj_data['dec']*u.deg)
                altaz = coord.transform_to(frame)
                
                alt = altaz.alt.degree
                az = altaz.az.degree
                
                obj_info = f"{obj_id} ({obj_data['name']}): {format_coordinates(alt, az)} - {obj_data['type']}"
                all_objects_info.append(obj_info)
                
                if is_visible(alt, min_altitude):
                    visible_objects.append(f"✓ {obj_info}")
                    
            except Exception as e:
                all_objects_info.append(f"{obj_id}: 计算错误 - {str(e)}")
        
        result = f"深空天体观测信息:\n"
        result += f"观测时间: {time.iso}\n"
        result += f"观测地点: {latitude:.2f}°, {longitude:.2f}°\n"
        result += f"最小可见高度角: {min_altitude}°\n"
        result += f"筛选类型: {object_type}\n\n"
        
        if visible_objects:
            result += f"当前可见的深空天体 ({len(visible_objects)}个):\n" + "\n".join(visible_objects)
        else:
            result += "当前没有深空天体在指定的可见范围内"
            
        result += f"\n\n所有查询天体位置 (共{len(all_objects_info)}个):\n" + "\n".join(all_objects_info)
        
        return result
        
    except Exception as e:
        return f"获取深空天体信息时发生错误: {str(e)}"

@mcp.tool()
async def get_bright_stars(latitude: float, longitude: float, time_str: str = None,
                         timezone_str: str = "UTC", min_altitude: float = 20.0) -> str:
    """获取当前可见的亮星
    
    Args:
        latitude: 纬度 (-90 to 90)
        longitude: 经度 (-180 to 180)
        time_str: 时间 (ISO格式，如 "2024-01-01T20:00:00", 默认为当前时间)
        timezone_str: 时区 (如 "Asia/Shanghai", 默认为 "UTC")
        min_altitude: 最小可见高度角 (度, 默认20度)
    """
    try:
        time = get_observation_time(time_str, timezone_str)
        location = get_location(latitude, longitude)
        frame = AltAz(obstime=time, location=location)
        
        visible_stars = []
        all_stars_info = []
        
        for star_id, star_data in BRIGHT_STARS.items():
            try:
                coord = SkyCoord(ra=star_data['ra']*u.deg, dec=star_data['dec']*u.deg)
                altaz = coord.transform_to(frame)
                
                alt = altaz.alt.degree
                az = altaz.az.degree
                
                star_info = f"{star_data['name']} ({star_id}): {format_coordinates(alt, az)} - 星等: {star_data['mag']}"
                all_stars_info.append(star_info)
                
                if is_visible(alt, min_altitude):
                    visible_stars.append(f"✓ {star_info}")
                    
            except Exception as e:
                all_stars_info.append(f"{star_id}: 计算错误 - {str(e)}")
        
        # 按高度角排序可见星星
        visible_stars.sort(key=lambda x: float(x.split("高度角: ")[1].split("°")[0]), reverse=True)
        
        result = f"亮星观测信息:\n"
        result += f"观测时间: {time.iso}\n"
        result += f"观测地点: {latitude:.2f}°, {longitude:.2f}°\n"
        result += f"最小可见高度角: {min_altitude}°\n\n"
        
        if visible_stars:
            result += f"当前可见的亮星 ({len(visible_stars)}颗，按高度角排序):\n" + "\n".join(visible_stars)
        else:
            result += "当前没有亮星在指定的可见范围内"
            
        result += f"\n\n所有查询亮星位置:\n" + "\n".join(all_stars_info)
        
        return result
        
    except Exception as e:
        return f"获取亮星信息时发生错误: {str(e)}"

@mcp.tool()
async def get_sun_info(latitude: float, longitude: float, time_str: str = None,
                      timezone_str: str = "UTC") -> str:
    """获取太阳的位置信息
    
    Args:
        latitude: 纬度 (-90 to 90)
        longitude: 经度 (-180 to 180)
        time_str: 时间 (ISO格式，如 "2024-01-01T20:00:00", 默认为当前时间)
        timezone_str: 时区 (如 "Asia/Shanghai", 默认为 "UTC")
    """
    try:
        time = get_observation_time(time_str, timezone_str)
        location = get_location(latitude, longitude)
        frame = AltAz(obstime=time, location=location)
        
        sun = get_sun(time)
        sun_altaz = sun.transform_to(frame)
        
        alt = sun_altaz.alt.degree
        az = sun_altaz.az.degree
        
        if alt > 0:
            status = "日间"
        elif alt > -6:
            status = "民用黄昏/黎明"
        elif alt > -12:
            status = "航海黄昏/黎明"
        elif alt > -18:
            status = "天文黄昏/黎明"
        else:
            status = "天文夜间"
        
        result = f"太阳信息:\n"
        result += f"观测时间: {time.iso}\n"
        result += f"观测地点: {latitude:.2f}°, {longitude:.2f}°\n"
        result += f"{format_coordinates(alt, az)}\n"
        result += f"天空状态: {status}"
        
        if alt < -18:
            result += " (最佳天文观测时间)"
        elif alt < -12:
            result += " (较好的天文观测时间)"
        elif alt < 0:
            result += " (一般的天文观测时间)"
        else:
            result += " (不适合天文观测)"
            
        return result
        
    except Exception as e:
        return f"获取太阳信息时发生错误: {str(e)}"

@mcp.tool()
async def get_observation_recommendations(latitude: float, longitude: float, time_str: str = None,
                                       timezone_str: str = "UTC") -> str:
    """获取当前时间和地点的天文观测推荐
    
    Args:
        latitude: 纬度 (-90 to 90)
        longitude: 经度 (-180 to 180)
        time_str: 时间 (ISO格式，如 "2024-01-01T20:00:00", 默认为当前时间)
        timezone_str: 时区 (如 "Asia/Shanghai", 默认为 "UTC")
    """
    try:
        time = get_observation_time(time_str, timezone_str)
        location = get_location(latitude, longitude)
        frame = AltAz(obstime=time, location=location)
        
        recommendations = []
        
        # 检查太阳位置
        sun = get_sun(time)
        sun_altaz = sun.transform_to(frame)
        sun_alt = sun_altaz.alt.degree
        
        if sun_alt > 0:
            recommendations.append("⚠️ 当前是白天，不适合天文观测")
            return f"观测建议:\n观测时间: {time.iso}\n观测地点: {latitude:.2f}°, {longitude:.2f}°\n\n" + "\n".join(recommendations)
        
        # 月亮信息
        moon = get_moon(time)
        moon_altaz = moon.transform_to(frame)
        moon_alt = moon_altaz.alt.degree
        
        if moon_alt > 20:
            sun_moon_sep = moon.separation(sun).degree
            if sun_moon_sep > 135:
                recommendations.append("🌙 月亮较亮，可能影响深空天体观测，但适合观测月亮细节")
            else:
                recommendations.append("🌙 月相较暗，有利于深空天体观测")
        
        # 可见行星
        visible_planets = []
        for planet in PLANETS:
            try:
                body = get_body(planet, time)
                altaz = body.transform_to(frame)
                if altaz.alt.degree > 20:
                    visible_planets.append(f"{planet.upper()}({altaz.alt.degree:.0f}°)")
            except:
                pass
        
        if visible_planets:
            recommendations.append(f"🪐 推荐观测行星: {', '.join(visible_planets)}")
        
        # 可见亮星
        visible_star_count = 0
        for star_data in BRIGHT_STARS.values():
            try:
                coord = SkyCoord(ra=star_data['ra']*u.deg, dec=star_data['dec']*u.deg)
                altaz = coord.transform_to(frame)
                if altaz.alt.degree > 20:
                    visible_star_count += 1
            except:
                pass
        
        if visible_star_count >= 3:
            recommendations.append(f"⭐ 当前可见{visible_star_count}颗亮星，适合星座观测")
        
        # 可见深空天体
        visible_dso_count = 0
        for obj_data in MESSIER_OBJECTS.values():
            try:
                coord = SkyCoord(ra=obj_data['ra']*u.deg, dec=obj_data['dec']*u.deg)
                altaz = coord.transform_to(frame)
                if altaz.alt.degree > 40:
                    visible_dso_count += 1
            except:
                pass
        
        if visible_dso_count >= 2:
            recommendations.append(f"🌌 当前有{visible_dso_count}个深空天体位置理想，推荐使用望远镜观测")
        
        # 天空条件评估
        if sun_alt < -18:
            recommendations.append("🌃 天文夜间，天空条件极佳")
        elif sun_alt < -12:
            recommendations.append("🌆 航海黄昏，天空条件良好")
        else:
            recommendations.append("🌅 民用黄昏，天空条件一般")
        
        if not recommendations:
            recommendations.append("当前观测条件有限，建议等待更好的时机")
        
        result = f"观测建议:\n"
        result += f"观测时间: {time.iso}\n"
        result += f"观测地点: {latitude:.2f}°, {longitude:.2f}°\n\n"
        result += "\n".join(recommendations)
        
        return result
        
    except Exception as e:
        return f"生成观测建议时发生错误: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

